<?php
/**
 * Travel Dervish: enquiry form handler (Hostinger shared hosting, PHP 7.4+)
 * The website is on Cloudflare Pages, which can't run PHP, so this file stays on Hostinger:
 *   public_html/travel-forms/send-enquiry.php  ->  https://designdervish.com/travel-forms/send-enquiry.php
 * Handles holiday-package, flight-ticket and flight + holiday enquiries.
 *
 * HOW EMAILS ARE SENT
 * designdervish.com email runs on Google Workspace, so enquiries are sent THROUGH GMAIL:
 *   1) In the Google account below, turn on 2-Step Verification (myaccount.google.com/security).
 *   2) Create an App Password: myaccount.google.com/apppasswords  (name it "Travel website").
 *   3) Paste the 16-letter password between the quotes in $SMTP_PASS below and save.
 * If $SMTP_PASS is empty, the server's own mail() is tried instead (often blocked or sent to Spam).
 * Any sending problem is written to mail-errors.log in this folder (open it in File Manager).
 */
$TO        = 'travel@designdervish.com';     // inbox that receives enquiries
$SMTP_USER = 'travel@designdervish.com';     // Google Workspace account that sends them (log-in email)
$SMTP_PASS = '';                             // its 16-letter App Password (spaces are fine)
$FROM      = 'no-reply@designdervish.com';   // sender used only by the mail() fallback
$SUBJECT_PREFIX = 'New enquiry';
$SITE = 'https://travel.designdervish.com/';  // where visitors are sent back to

function back($q) { global $SITE; header('Location: ' . $SITE . $q, true, 303); exit; }
function logf($msg) { @file_put_contents(__DIR__ . '/mail-errors.log', date('c') . '  ' . $msg . "\n", FILE_APPEND | LOCK_EX); }

// Only accept forms sent from the Travel Dervish site or its Cloudflare preview addresses
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '' && $origin !== 'null') {
    $host = (string)parse_url($origin, PHP_URL_HOST);
    $allowed = in_array($host, ['travel.designdervish.com', 'designdervish.com', 'www.designdervish.com'], true)
               || preg_match('/(^|[.-])travel-?dervish\.(pages\.dev|initishmalik\.workers\.dev)$/', $host);
    if (!$allowed) back('contact');
}
function clean($v, $max = 500) {
    $v = trim((string)$v);
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);   // block header injection
    return mb_substr(strip_tags($v), 0, $max);
}
function field($name, $max = 120) { return clean($_POST[$name] ?? '', $max); }
function show($v) { return $v !== '' ? $v : '-'; }
function hdr($text) { return '=?UTF-8?B?' . base64_encode($text) . '?='; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') back('contact');

// Honeypot: real visitors never fill this hidden field
if (!empty($_POST['website'])) back('thank-you');

$name       = field('name', 120);
$email      = field('email', 160);
$phone      = field('phone', 40);
$service    = field('service', 20);
$journey    = field('journey', 60);
$month      = field('month', 20);
$travellers = field('travellers', 10);
$style      = field('style', 40);
$from       = field('from', 80);
$to         = field('to', 80);
$trip       = field('trip', 20);
$depart     = field('depart', 20);
$return     = field('return', 20);
$cabin      = field('cabin', 30);
$pageFrom   = field('page', 40);
$message    = mb_substr(trim(strip_tags((string)($_POST['message'] ?? ''))), 0, 3000);

if (!in_array($service, ['package', 'flight', 'both'], true)) $service = ($from !== '' || $to !== '') ? 'flight' : 'package';
$services = ['package' => 'Holiday package', 'flight' => 'Flight tickets', 'both' => 'Flight + holiday'];
$journeys = ['rajasthan' => 'Rajasthan Heritage Tour (16D/15N)', 'thailand' => 'Thailand Holiday (5D/4N)', 'custom' => 'Custom trip / not sure yet'];
$trips    = ['return' => 'Round trip', 'oneway' => 'One way', 'multicity' => 'Multi-city'];
$journeyLabel = $journeys[$journey] ?? ($journey !== '' ? $journey : 'Not specified');

$pages = ['rajasthan' => 'rajasthan-heritage-tour?error=1#enquire', 'thailand' => 'thailand-holiday-package?error=1#enquire',
          'flights' => 'flights?error=1#request'];
$back = $pages[$pageFrom] ?? 'contact?error=1#form';

if ($name === '' || $phone === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) back($back);
if ($service === 'flight' && ($from === '' || $to === '')) back($back);

$body  = "New enquiry from the Travel Dervish website\n";
$body .= "--------------------------------------------\n";
$body .= "Service:      " . $services[$service] . "\n";
$body .= "Name:         $name\n";
$body .= "Email:        $email\n";
$body .= "Phone:        $phone\n";
$body .= "Travellers:   " . show($travellers) . "\n";
if ($service !== 'flight') {
    $body .= "\nHOLIDAY\n";
    $body .= "Journey:      $journeyLabel\n";
    $body .= "Travel month: " . show($month) . "\n";
    $body .= "Trip style:   " . show($style) . "\n";
}
if ($service !== 'package') {
    $body .= "\nFLIGHT\n";
    $body .= "From:         " . show($from) . "\n";
    $body .= "To:           " . show($to) . "\n";
    $body .= "Trip type:    " . ($trips[$trip] ?? show($trip)) . "\n";
    $body .= "Departure:    " . show($depart) . "\n";
    $body .= "Return:       " . show($return) . "\n";
    $body .= "Cabin:        " . show($cabin) . "\n";
}
$body .= "\nSent from:    " . show($pageFrom) . " page\n\n";
$body .= "Message:\n" . show($message) . "\n";
$body = str_replace("\n", "\r\n", $body);

$what = ($service === 'flight') ? "Flights $from to $to" : $journeyLabel;
if ($service === 'both') $what .= ' + flights';
$subject = "$SUBJECT_PREFIX: $what - $name";
$encodedBody = rtrim(chunk_split(base64_encode($body), 76, "\r\n"));

/** Sends through Gmail (smtp.gmail.com, TLS + App Password). Returns true or an error text. */
function smtp_send($user, $pass, $to, $data) {
    $attempts = [['tcp://smtp.gmail.com:587', true], ['ssl://smtp.gmail.com:465', false]];
    $last = 'no connection';
    foreach ($attempts as [$addr, $starttls]) {
        $fp = @stream_socket_client($addr, $errno, $errstr, 20);
        if (!$fp) { $last = "connect $addr failed: $errstr"; continue; }
        stream_set_timeout($fp, 25);
        $read = function () use ($fp) {
            $resp = '';
            while (($line = fgets($fp, 515)) !== false) { $resp .= $line; if (strlen($line) < 4 || $line[3] === ' ') break; }
            return $resp;
        };
        // $label is what the log shows for this step: never the username/password or the message itself
        $cmd = function ($c, $codes, $label = null) use ($fp, $read) {
            if ($c !== null) fwrite($fp, $c . "\r\n");
            $r = $read();
            if (!in_array((int)substr($r, 0, 3), (array)$codes, true)) {
                throw new Exception(($label ?? ($c ?? 'greeting')) . ' -> ' . trim($r));
            }
            return $r;
        };
        try {
            $cmd(null, 220);
            $cmd('EHLO travel.designdervish.com', 250);
            if ($starttls) {
                $cmd('STARTTLS', 220);
                if (!stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) throw new Exception('TLS start failed');
                $cmd('EHLO travel.designdervish.com', 250);
            }
            $cmd('AUTH LOGIN', 334);
            $cmd(base64_encode($user), 334, 'username');
            $cmd(base64_encode(str_replace(' ', '', $pass)), 235, 'password (check the App Password)');
            $cmd("MAIL FROM:<$user>", 250);
            $cmd("RCPT TO:<$to>", [250, 251]);
            $cmd('DATA', 354);
            $cmd(preg_replace('/^\./m', '..', $data) . "\r\n.", 250, 'message');
            @fwrite($fp, "QUIT\r\n");
            fclose($fp);
            return true;
        } catch (Exception $e) {
            $last = "$addr: " . $e->getMessage();
            @fclose($fp);
        }
    }
    return $last;
}

$sent = false;
if ($SMTP_PASS !== '') {
    $data = implode("\r\n", [
        'Date: ' . date('r'),
        'From: ' . hdr('Travel Dervish Website') . " <$SMTP_USER>",
        "To: <$TO>",
        'Reply-To: ' . hdr($name) . " <$email>",
        'Subject: ' . hdr($subject),
        'Message-ID: <' . bin2hex(random_bytes(10)) . '@designdervish.com>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ]) . "\r\n\r\n" . $encodedBody;
    $r = smtp_send($SMTP_USER, $SMTP_PASS, $TO, $data);
    if ($r === true) $sent = true; else logf('Gmail: ' . $r);
} else {
    logf('Gmail App Password not set in send-enquiry.php; trying the server mail() instead');
}

if (!$sent) {   // fallback: the server's own mail()
    $headers  = 'From: ' . hdr('Travel Dervish Website') . " <$FROM>\r\n";
    $headers .= 'Reply-To: ' . hdr($name) . " <$email>\r\n";
    $headers .= "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64";
    $sent = @mail($TO, hdr($subject), $encodedBody, $headers, '-f' . $FROM)
         || @mail($TO, hdr($subject), $encodedBody, $headers);
    if (!$sent) { $err = error_get_last(); logf('mail() failed' . ($err ? ': ' . $err['message'] : '')); }
}

back($sent ? 'thank-you' : $back);
