"""Travel Dervish: all editable site content lives in this file.
Change contact details, packages, destinations or FAQs here, then run:  python _builder/build.py
"""

# ----------------------------------------------------------------------------------
# 1) SITE SETTINGS
# ----------------------------------------------------------------------------------
SITE = {
    "name": "Travel Dervish",
    "url": "https://travel.designdervish.com",
    "tagline": "Your Travel Partner for Every Journey",
    "phone_display": "+91 99105 61078",
    "phone_link": "+919910561078",
    "email": "travel@designdervish.com",       # the brand poster says "designdrvish.com": that looks like a typo
    "city": "Delhi, India",
    # WhatsApp is switched OFF for now. To turn it on later: set show_whatsapp to True and rebuild.
    "show_whatsapp": False,
    "whatsapp": "919910561078",                # country code + number, digits only (confirm before switching on)
    "instagram": "https://www.instagram.com/",   # TODO: your Instagram profile
    "facebook": "https://www.facebook.com/",     # TODO: your Facebook page
    "pinterest": "https://www.pinterest.com/",   # TODO: your Pinterest profile
    "parent": "https://www.designdervish.com",
    # The enquiry forms post to this PHP file on Hostinger (the site itself is on Cloudflare Pages, which can't run PHP).
    # Upload hostinger-forms/send-enquiry.php to public_html/travel-forms/ on Hostinger.
    "form_endpoint": "https://designdervish.com/travel-forms/send-enquiry.php",
}

# ----------------------------------------------------------------------------------
# 2) HOME BANNER: one chapter per Google Flow clip (files in website/assets/video/<key>-hd.mp4 and -sm.mp4)
# ----------------------------------------------------------------------------------
HERO_CHAPTERS = [
    # (video key, label, scope, line)
    ("desert", "Desert trails", "India", "Golden dunes &amp; camel caravans"),
    ("bay", "Island escapes", "International", "Turquoise bays &amp; longtail boats"),
    ("lake", "Lake cities", "India", "Palaces reflected at sunset"),
    ("fort", "Royal forts", "India", "Hilltop forts above still water"),
]

# Airports suggested in the flight forms (visitors can still type any city)
AIRPORTS = [
    ("Delhi", "DEL"), ("Mumbai", "BOM"), ("Bengaluru", "BLR"), ("Chennai", "MAA"), ("Kolkata", "CCU"), ("Hyderabad", "HYD"),
    ("Ahmedabad", "AMD"), ("Pune", "PNQ"), ("Goa", "GOI"), ("Kochi", "COK"), ("Jaipur", "JAI"), ("Udaipur", "UDR"),
    ("Jodhpur", "JDH"), ("Varanasi", "VNS"), ("Amritsar", "ATQ"), ("Srinagar", "SXR"), ("Leh", "IXL"), ("Bagdogra", "IXB"),
    ("Port Blair", "IXZ"), ("Dubai", "DXB"), ("Abu Dhabi", "AUH"), ("Bangkok", "BKK"), ("Phuket", "HKT"), ("Singapore", "SIN"),
    ("Kuala Lumpur", "KUL"), ("Bali (Denpasar)", "DPS"), ("Male (Maldives)", "MLE"), ("Colombo", "CMB"), ("Kathmandu", "KTM"),
    ("Hong Kong", "HKG"), ("Tokyo", "NRT"), ("Istanbul", "IST"), ("London", "LHR"), ("Paris", "CDG"), ("Frankfurt", "FRA"),
    ("Zurich", "ZRH"), ("New York", "JFK"), ("Toronto", "YYZ"), ("Sydney", "SYD"), ("Melbourne", "MEL"),
]

# ----------------------------------------------------------------------------------
# 3) PACKAGES (content from the two PDF itineraries)
#    type: "india" or "international" · video: a banner clip key, or None to use the card photo with 3D motion
# ----------------------------------------------------------------------------------
PACKAGES = [
    {
        "slug": "rajasthan", "file": "rajasthan-heritage-tour.html", "type": "india", "region": "India Journeys",
        "title": "Rajasthan Heritage, Culture & Wildlife Tour", "short": "Rajasthan Heritage Tour",
        "duration": "16 Days / 15 Nights", "days_n": 16, "dest_n": 10, "badge": "Signature", "badge_cls": "badge--sun",
        "video": "fort", "ends": ("Delhi", "Agra"), "via": "via 9 stops",
        "tagline": "Delhi · Shekhawati · Thar Desert · Lakes · Tigers · Taj Mahal",
        "location": "Delhi, Rajasthan, Ranthambore & Agra",
        "categories": ["Heritage", "Cultural", "Desert", "Wildlife", "Leisure"],
        "styles": "heritage desert wildlife culture",
        "card_img": "card-rajasthan", "card_alt": "Amber Fort above Maota Lake, Jaipur",
        "summary": "Painted havelis, golden desert forts, the Blue City, lakeside Udaipur, a tiger safari and sunrise at the Taj Mahal — one well-paced loop.",
        "overview": ("A 16-day journey through India&rsquo;s most colourful state. Start in Old and New Delhi, drive into the "
                     "painted towns of Shekhawati, cross the Thar Desert to golden Jaisalmer and the dunes of Sam, then continue "
                     "through blue Jodhpur, the marble temples of Ranakpur and the lakes of Udaipur. Slow down in holy Pushkar, "
                     "eat your way through Jaipur&rsquo;s bazaars, look for tigers in Ranthambore and finish with sunrise at the "
                     "Taj Mahal before heading back to Delhi."),
        "route": ["Delhi", "Nawalgarh", "Bikaner", "Jaisalmer", "Jodhpur", "Udaipur", "Pushkar", "Jaipur", "Ranthambore", "Agra", "Delhi"],
        "route_days": ["D1", "D3", "D4", "D5", "D7", "D8", "D10", "D11", "D13", "D15", "D16"],
        "facts": [("calendar", "Duration", "16 Days / 15 Nights"), ("map", "Destinations", "10 stops, Delhi to Agra"),
                  ("car", "Transport", "Private vehicle as per group size"), ("bed", "Stays", "As per selected hotel category")],
        "highlights": [
            "Explore the historical monuments and vibrant markets of Delhi",
            "Discover the traditional painted havelis of Shekhawati",
            "Visit the famous Karni Mata Temple at Deshnoke",
            "Experience the golden beauty of Jaisalmer and its desert landscapes",
            "Enjoy an optional camel safari at Sam Sand Dunes",
            "Explore the magnificent Mehrangarh Fort in Jodhpur",
            "Discover the architectural beauty of Ranakpur Jain Temple",
            "Enjoy a scenic boat ride on Lake Pichola in Udaipur",
            "Experience the spiritual atmosphere of Pushkar",
            "Discover Jaipur&rsquo;s colourful bazaars and traditional cuisine",
            "Enjoy a wildlife safari at Ranthambore National Park",
            "Witness the sunrise at the Taj Mahal in Agra",
        ],
        "gallery": [("gal-amber-fort", "Amber Fort, Jaipur"), ("gal-hawa-mahal", "Hawa Mahal, Jaipur"),
                    ("gal-udaipur-lake", "Lake Palace on Lake Pichola, Udaipur"), ("gal-camel-sunset", "Camel caravan, Sam Sand Dunes"),
                    ("gal-tiger", "Bengal tiger, Ranthambore"), ("gal-jodhpur-blue", "Blue lanes of Jodhpur"),
                    ("gal-mehrangarh", "Mehrangarh Fort, Jodhpur"), ("gal-jama-masjid", "Jama Masjid, Old Delhi"),
                    ("gal-taj-mahal", "Taj Mahal, Agra")],
        "days": [
            ("Arrival in Delhi", "", "", ["Upon arrival at Delhi International Airport, you will be warmly welcomed by our representative and transferred to your hotel. Check in and relax after your journey."], "Delhi (pre-night accommodation)", None),
            ("Old &amp; New Delhi sightseeing", "", "", ["After breakfast, set out on a cultural tour of Old Delhi. Visit Jama Masjid, one of India&rsquo;s largest and most famous mosques, followed by Rajghat, the memorial dedicated to Mahatma Gandhi.", "Enjoy a traditional cycle-rickshaw ride through the lively lanes of Chandni Chowk, explore the famous Spice Market and stop for a cup of Indian chai. Walk back past the Red Fort, then drive through New Delhi to India Gate and the Government Buildings."], "Delhi", ("gal-jama-masjid", "Jama Masjid, Old Delhi")),
            ("Delhi &ndash; Nawalgarh", "290 km", "5&ndash;6 hrs", ["After breakfast, drive to Nawalgarh in the historic Shekhawati region. In the afternoon, explore the area&rsquo;s beautifully painted havelis, traditional frescoes and heritage architecture."], "Nawalgarh", None),
            ("Nawalgarh &ndash; Deshnoke &ndash; Bikaner", "224 km", "3&ndash;4 hrs", ["Drive towards Bikaner, stopping at Deshnoke village to visit the famous Karni Mata Temple, popularly known as the Rat Temple.", "In the afternoon, visit Junagarh Fort, a magnificent showcase of Rajasthan&rsquo;s royal architecture, then the Camel Breeding Centre to learn about the camel&rsquo;s role in desert life."], "Bikaner", None),
            ("Bikaner &ndash; Khichan &ndash; Jaisalmer", "329 km", "5&ndash;6 hrs", ["Drive to Jaisalmer, the Golden City. En route, visit Khichan village, famous for the migratory Demoiselle Cranes that gather here in large numbers in winter. Evening at leisure in Jaisalmer."], "Jaisalmer", None),
            ("Jaisalmer Fort &amp; Sam Sand Dunes", "", "", ["Explore the magnificent Jaisalmer Fort and its heritage havelis, famous for their intricate sandstone carvings.", "Later, drive to Sam Sand Dunes in the Thar Desert. Opt for a traditional camel safari to watch the sunset over the dunes, followed by dinner and the desert experience. Camel safari charges are optional and payable directly."], "Jaisalmer", ("gal-camel-sunset", "Camel caravan at Sam Sand Dunes")),
            ("Jaisalmer &ndash; Jodhpur", "273 km", "5 hrs", ["Drive to Jodhpur, the Blue City. In the afternoon, visit Mehrangarh Fort and its museum, showcasing the royal history of Jodhpur, then explore the colourful local bazaar near the fort."], "Jodhpur", ("gal-mehrangarh", "Mehrangarh Fort above Jodhpur")),
            ("Jodhpur &ndash; Ranakpur &ndash; Udaipur", "264 km", "4 hrs", ["Drive towards Udaipur, the City of Lakes. En route, visit the Chaumukha Jain Temple at Ranakpur, renowned for its marble architecture and intricately carved pillars, with a guided tour by an English-speaking priest."], "Udaipur", None),
            ("Udaipur &amp; Lake Pichola", "", "", ["Begin with a walk through the local vegetable market, then visit City Palace, Bharatiya Lok Kala Mandal, Saheliyon Ki Bari and the Maharana Pratap Memorial.", "In the afternoon, take a boat ride on Lake Pichola to Jag Mandir Island Palace, then relax at a lakeside caf&eacute; with tea or coffee as the sun sets."], "Udaipur", ("gal-udaipur-lake", "Lake Pichola, Udaipur")),
            ("Udaipur &ndash; Pushkar", "280 km", "5 hrs", ["Drive to Pushkar, one of India&rsquo;s most sacred pilgrimage towns. Explore the old town and the Brahma Temple, then join a traditional ceremony at Pushkar Lake conducted by a local priest."], "Pushkar", None),
            ("Pushkar &ndash; Jaipur", "148 km", "3 hrs", ["Drive to Jaipur, the Pink City, for a walking and food tour with a cycle-rickshaw ride through the bazaars, a look at the spices of Indian cooking and local delicacies.", "In the evening, visit Nahargarh Fort for sunset views over the illuminated city."], "Jaipur", ("gal-hawa-mahal", "Hawa Mahal, Jaipur")),
            ("Jaipur: Amber Fort &amp; city", "", "", ["Visit Amber Fort and its decorated palace complex, including the famous Sheesh Mahal (Hall of Mirrors).", "Back in Jaipur, continue to City Palace, Hawa Mahal (Palace of Winds) and Jantar Mantar, the historic astronomical observatory and UNESCO World Heritage Site."], "Jaipur", ("gal-amber-fort", "Amber Fort, Jaipur")),
            ("Jaipur &ndash; Ranthambore", "179 km", "4 hrs", ["Drive to Ranthambore National Park, one of India&rsquo;s most famous wildlife destinations. Check in at the wildlife resort and spend the rest of the day relaxing."], "Ranthambore", None),
            ("Ranthambore wildlife safari", "", "", ["Head out on a scheduled jungle safari through the habitat of the Bengal tiger. Depending on luck and season, you may spot tigers, leopards, sloth bears, crocodiles, deer and many bird species. All meals are served at the resort."], "Ranthambore", ("gal-tiger", "Bengal tiger, Ranthambore")),
            ("Ranthambore &ndash; Fatehpur Sikri &ndash; Agra", "310 km", "5&ndash;6 hrs", ["Drive to Agra, visiting Fatehpur Sikri on the way &mdash; the Mughal city built by Emperor Akbar in the 16th century, with its impressive Buland Darwaza."], "Agra", None),
            ("Taj Mahal sunrise &ndash; Delhi departure", "248 km", "4 hrs", ["Visit the Taj Mahal at sunrise, return for breakfast and a late check-out around 11:00 AM. After lunch, visit Agra Fort, then drive back to Delhi with a refreshment break en route and transfer to the airport for your onward flight."], "Tour ends with wonderful memories", ("gal-taj-mahal", "Taj Mahal, Agra")),
        ],
        "table": [("Duration", "16 Days / 15 Nights"), ("Destinations", "Delhi, Nawalgarh, Bikaner, Jaisalmer, Jodhpur, Udaipur, Pushkar, Jaipur, Ranthambore and Agra"),
                  ("Tour type", "Cultural, Heritage, Wildlife and Leisure"), ("Accommodation", "As per selected hotel category"),
                  ("Transportation", "Private vehicle as per group size"), ("Special experiences", "Local food tour, camel safari, temple visit, boat ride and wildlife safari")],
        "notes": ["The Taj Mahal is closed every Friday.", "Khichan bird sightings are seasonal and cannot be guaranteed.",
                  "Camel safari charges at Sam Sand Dunes are optional and payable directly."],
        "pdf": "assets/pdf/rajasthan-heritage-tour-16d-15n.pdf",
        "meta": "16-day Rajasthan heritage, culture and wildlife tour from Delhi: Shekhawati, Bikaner, Jaisalmer, Jodhpur, Udaipur, Pushkar, Jaipur, Ranthambore and the Taj Mahal.",
    },
    {
        "slug": "thailand", "file": "thailand-holiday-package.html", "type": "international", "region": "International Escapes",
        "title": "Thailand Holiday: Bangkok, Pattaya & Koh Larn", "short": "Thailand Holiday Package",
        "duration": "5 Days / 4 Nights", "days_n": 5, "dest_n": 3, "badge": "Beach &amp; City", "badge_cls": "badge--ember",
        "video": "bay", "ends": ("Bangkok", "Koh Larn"), "via": "via Pattaya",
        "tagline": "Temples · Chinatown · Sanctuary of Truth · Coral Island",
        "location": "Bangkok, Pattaya & Koh Larn, Thailand",
        "categories": ["Leisure", "Beach", "City", "Culture"],
        "styles": "beach city culture",
        "card_img": "card-thailand", "card_alt": "Wat Arun at sunset, Bangkok",
        "summary": "Bangkok&rsquo;s Grand Palace and Wat Arun, Chinatown street food, Pattaya&rsquo;s Sanctuary of Truth and a ferry to Coral Island.",
        "overview": ("Discover the vibrant charm of Thailand on a holiday that combines Bangkok&rsquo;s cultural heritage, "
                     "magnificent temples and bustling markets with Pattaya&rsquo;s beaches and best-known attractions. Explore "
                     "the best of city life, island beauty and tropical gardens in five easy days."),
        "route": ["Bangkok", "Chao Phraya", "Pattaya", "Koh Larn", "Nong Nooch", "Bangkok Airport"],
        "route_days": ["D1", "D2", "D3", "D4", "D4", "D5"],
        "facts": [("calendar", "Duration", "5 Days / 4 Nights"), ("map", "Destinations", "Bangkok, Pattaya, Koh Larn"),
                  ("sun", "Tour type", "Leisure"), ("boat", "Island day", "Ferry to Koh Larn (Coral Island)")],
        "highlights": [
            "Explore Bangkok&rsquo;s famous Grand Palace, Wat Pho and Wat Arun",
            "Experience the traditional charm of Bangkok&rsquo;s Chinatown",
            "Discover Pattaya&rsquo;s spectacular Sanctuary of Truth",
            "Enjoy a ferry excursion to the beautiful Koh Larn Island",
            "Explore the lush landscapes of Nong Nooch Tropical Garden",
            "Experience Thailand&rsquo;s vibrant local markets and street-food culture",
        ],
        "gallery": [("gal-wat-arun", "Wat Arun at sunset, Bangkok"), ("gal-grand-palace", "Grand Palace, Bangkok"),
                    ("gal-koh-larn-beach", "Turquoise water and longtail boat"), ("gal-sanctuary-of-truth", "Sanctuary of Truth, Pattaya"),
                    ("gal-chinatown", "Tuk-tuks in Chinatown, Bangkok"), ("gal-street-food", "Thai street-food market"),
                    ("gal-yaowarat-neon", "Yaowarat Road at night"), ("gal-thai-bay", "Thai bay with longtail boats"),
                    ("gal-longtail", "Longtail boat ride")],
        "days": [
            ("Arrival in Bangkok", "", "", ["Upon arrival at Suvarnabhumi International Airport, you will be welcomed and transferred to your hotel in Bangkok. After check-in, take some time to relax.", "Later, explore Bangkok at your leisure &mdash; shop at Pratunam Market or soak up the nightlife and street food of Khaosan Road, with dinner at a local street-food stall."], "Bangkok", ("gal-yaowarat-neon", "Bangkok at night")),
            ("Bangkok city tour &ndash; temples &amp; Chao Phraya River", "", "", ["After breakfast, visit the magnificent Grand Palace, then Wat Pho with its impressive Reclining Buddha. Take a short ferry across the Chao Phraya River to Wat Arun (Temple of Dawn) and its beautifully decorated central tower.", "In the afternoon, ride the Chao Phraya Express Boat to Chinatown and explore Yaowarat Road, known for its colourful markets, local delicacies and street food."], "Bangkok", ("gal-wat-arun", "Wat Arun on the Chao Phraya River")),
            ("Bangkok &ndash; Pattaya &amp; Sanctuary of Truth", "", "", ["Check out and transfer to Pattaya, a popular beach destination. After check-in, visit the Sanctuary of Truth, an extraordinary wooden masterpiece of hand-carved sculptures inspired by Thai art, philosophy and culture.", "In the evening, stroll along Pattaya Beach Road, explore the night markets and enjoy Thai street food."], "Pattaya", ("gal-sanctuary-of-truth", "Sanctuary of Truth, Pattaya")),
            ("Koh Larn island &amp; Nong Nooch Tropical Garden", "", "", ["Board a public ferry from Bali Hai Pier to Koh Larn (Coral Island), known for its crystal-clear water and white-sand beaches. Spend leisure time at Tawaen or Samae Beach &mdash; swim, relax, or try optional water activities at your own expense.", "Back in Pattaya, visit Nong Nooch Tropical Garden with its landscaped gardens, Dinosaur Valley and cultural performances (subject to ticket package and show schedule). End the day at Jomtien Beach for seafood by the sea."], "Pattaya", ("gal-koh-larn-beach", "Clear water at Koh Larn")),
            ("Pattaya &ndash; Bangkok Airport departure", "", "", ["After breakfast, check out and transfer to Bangkok International Airport for your scheduled flight, with wonderful memories of your Thailand holiday."], "Tour ends with happy memories", None),
        ],
        "table": [("Duration", "5 Days / 4 Nights"), ("Destinations", "Bangkok, Pattaya and Koh Larn"), ("Tour category", "Leisure"),
                  ("Sightseeing", "Grand Palace, Wat Pho, Wat Arun, Chinatown, Sanctuary of Truth, Koh Larn, Nong Nooch Tropical Garden"),
                  ("Island excursion", "Public ferry from Bali Hai Pier to Koh Larn (Coral Island)")],
        "notes": ["Water activities on Koh Larn are optional and at your own expense.",
                  "Nong Nooch attractions and shows depend on the selected ticket package and show schedule.",
                  "The departure transfer is timed to your scheduled flight."],
        "pdf": "assets/pdf/thailand-holiday-package-5d-4n.pdf",
        "meta": "5-day Thailand holiday: Bangkok's Grand Palace, Wat Pho and Wat Arun, Chinatown, Pattaya's Sanctuary of Truth, Koh Larn (Coral Island) and Nong Nooch Garden.",
    },
]

DESTINATIONS = [
    ("dest-delhi", "Delhi", "India", "Old &amp; New Delhi", "rajasthan"),
    ("dest-jaisalmer", "Jaisalmer", "India", "The Golden City", "rajasthan"),
    ("dest-jodhpur", "Jodhpur", "India", "The Blue City", "rajasthan"),
    ("dest-udaipur", "Udaipur", "India", "City of Lakes", "rajasthan"),
    ("dest-jaipur", "Jaipur", "India", "The Pink City", "rajasthan"),
    ("dest-ranthambore", "Ranthambore", "India", "Tiger country", "rajasthan"),
    ("dest-agra", "Agra", "India", "The Taj Mahal", "rajasthan"),
    ("dest-bangkok", "Bangkok", "Thailand", "Temples &amp; Chinatown", "thailand"),
    ("dest-pattaya", "Pattaya", "Thailand", "Sanctuary of Truth", "thailand"),
    ("dest-koh-larn", "Koh Larn", "Thailand", "Coral Island beaches", "thailand"),
]

FAQS = [
    ("How do I book with Travel Dervish?", "Send an enquiry through the form or call us with your dates and the number of travellers. For a holiday we reply with a day-by-day plan and quote; for flights, with fare options."),
    ("Do you book flight tickets on their own?", "Yes. Share your route, travel dates, number of travellers and cabin class, and we&rsquo;ll come back with fare options before anything is booked."),
    ("Can the itinerary be adjusted?", "Yes. The itineraries on this site are starting points &mdash; tell us what you&rsquo;d like to add, skip or slow down and we&rsquo;ll update the plan and quote."),
    ("What kind of hotels are included?", "Accommodation is as per the hotel category you select. Share your preference when you enquire and we&rsquo;ll plan around it."),
    ("Is the camel safari at Sam Sand Dunes included?", "The camel safari on the Rajasthan journey is optional and payable directly on the day."),
    ("Are there days when sights are closed?", "The Taj Mahal is closed every Friday, so the Agra day is planned around it. Khichan crane sightings are seasonal and can&rsquo;t be guaranteed."),
    ("Are water activities on Koh Larn included?", "Beach time on Koh Larn is part of the Thailand holiday; water activities are optional and at your own expense."),
]

FLIGHT_FAQS = [
    ("Which flights can you book?", "Domestic flights within India and international flights. Tell us your route and dates and we&rsquo;ll share the options."),
    ("What details do you need for a fare quote?", "Your route, travel dates (and whether they&rsquo;re flexible), the number of adults, children and infants, and the cabin class you prefer."),
    ("Can you combine flights with a holiday package?", "Yes. Many travellers book the flight and the holiday together &mdash; choose &ldquo;Flight + holiday&rdquo; on the enquiry form."),
]
