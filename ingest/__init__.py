from datetime import timedelta, timezone

# IESO publishes everything in Eastern Standard Time, all year.
# No daylight saving shift. Never use America/Toronto for IESO data.

EST = timezone(timedelta(hours=-5), name="EST")

