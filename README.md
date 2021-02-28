# app-store-reviews
Still under development!

Python command line tool to access user reviews from [Google Play](https://play.google.com/)
and [iTunes Store](https://itunes.apple.com).

Inspired by:
 - [app-store-scraper](https://github.com/facundoolano/app-store-scraper)
 - [google-play-scraper ](https://github.com/facundoolano/google-play-scraper)

# How to get AppStore ID
 -  Search in the desired app https://apps.apple.com and extract the id from the las part of the id. For example for WhatsApp: https://apps.apple.com/us/app/whatsapp-messenger/id310633997. The id is 310633997. 

# How to get GooglePlay ID

# Contribute
Want to contribute? :clap: Just fork and make a PR :thumbsup:

## TODO´s

Open to suggestions

- [ ] Code TODOs
- [ ] Documentation
- [ ] Tests
- [ ] Examples
- [ ] Find App Ids

### Dependencies
The functionality of this module is dependent of the existence and the
format as today (15.07.2018) form the following services:

- RSS feed from Apple feedback: https://itunes.apple.com/{contry_code}/rss/customerreviews/page={page_num}/id={itunes_id}
- Google Play Store GetReviews: https://play.google.com/store/getreviews
