# Real Estate Agent MVP

Israeli real estate agent that learns preferences, searches Yad2/Madlan daily, and sends personalized updates.

## What's Built

✅ **Landing Page** - Hebrew, warm, Israeli market feel
✅ **Onboarding Flow** - 6-step wizard collecting:
  - Search type (buy/rent)
  - Locations (cities + neighborhoods)
  - Budget range
  - Room count
  - Must-haves & deal-breakers
  - Contact info

✅ **Dashboard** - Activity feed showing agent "working"
✅ **Database** - SQLite storing users + preferences

## Stack

- Flask (Python)
- SQLite
- Tailwind CSS (via CDN)
- Hebrew RTL interface

## Run Locally

```bash
cd real-estate-agent
python app.py
```

Visit: http://localhost:5001

## Database

SQLite file: `agent.db`
- `users` table: email, name, phone
- `preferences` table: all search criteria

## What's Next (Not Built Yet)

1. **Web Scraping** - Yad2/Madlan scrapers (likely to be blocked, needs workaround)
2. **Matching Logic** - Compare scraped properties to user preferences
3. **Email System** - Daily/weekly email generation with Claude API
4. **Property Display** - Show matched properties on dashboard
5. **Scheduling** - Daily cron job for automated searches

## Key Files

- `app.py` - Flask app + API routes + DB setup
- `templates/landing.html` - Homepage
- `templates/onboarding.html` - 6-step wizard
- `templates/dashboard.html` - User activity feed

## Notes for You (Miki)

**Immediate Issues to Address:**

1. **Scraping Reality Check** - Yad2/Madlan will likely block scrapers. Options:
   - Use their mobile APIs (reverse-engineer network calls)
   - Pay for official APIs (if available)
   - Manual RSS/alerts initially
   - Browser automation (slower, fragile)

2. **Email Deliverability** - For friends group:
   - Start with SendGrid free tier (100 emails/day)
   - Use your own domain for better deliverability
   - Don't use gmail SMTP (gets flagged)

3. **Claude API Integration** - Need to add:
   - Personalized email generation
   - Property descriptions rewriting
   - Match explanation ("why this fits you")

**Testing Plan:**

1. Complete onboarding flow yourself
2. Check database has your data: `sqlite3 agent.db "SELECT * FROM users;"`
3. Mock some properties, test matching logic
4. Generate one email manually, send to yourself
5. Invite 2-3 friends, iterate based on feedback

**Cost Estimate (10 users for 1 month):**

- Hosting: $0 (start local or free tier)
- Claude API: ~$5-10 (email generation)
- SendGrid: $0 (free tier)
- Total: ~$10/month

**If scraping breaks:** Consider starting with manual property curation - you find 3-5 properties daily, paste URLs, system sends them with Claude-generated personalization. Less sexy, but proves the "caring agent" feeling.

**This is an MVP.** Ship it to friends, see if they open emails, see if they click. That tells you everything.
