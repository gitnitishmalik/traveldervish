<?php
/**
 * Travel Dervish: enquiry form handler (Hostinger shared hosting, PHP 7.4+)
 * The website itself is on Cloudflare Pages, which can't run PHP, so this one file stays on Hostinger:
 * upload it to  public_html/travel-forms/send-enquiry.php  ->  https://designdervish.com/travel-forms/send-enquiry.php
 * Handles holiday-package, flight-ticket and flight + holiday enquiries.
 * 1) $TO is the mailbox that receives enquiries.
 * 2) $FROM must be an address on your own domain (Hostinger requires the sender to be on a domain you host).
 */
$TO   = 'travel@designdervish.com';      // inbox that receives enquiries
$FROM = 'no-reply@designdervish.com';    // an address on your domain
$SUBJECT_PREFIX = 'New enquiry';
$SITE = 'https://travel.designdervish.com/';   // where visitors are sent back to

function back($q) { global $SITE; header('Location: ' . $SITE . $q, true, 303); exit; }

// Only accept forms sent from the Travel Dervish site or its Cloudflare preview addresses
// (traveldervish.pages.dev, traveldervish.initishmalik.workers.dev and their preview copies)
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

$what = ($service === 'flight') ? "Flights $from to $to" : $journeyLabel;
if ($service === 'both') $what .= ' + flights';
$subject = "$SUBJECT_PREFIX: $what - $name";
$headers  = "From: Travel Dervish Website <$FROM>\r\n";
$headers .= "Reply-To: $name <$email>\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$ok = @mail($TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $FROM);
back($ok ? 'thank-you' : $back);
