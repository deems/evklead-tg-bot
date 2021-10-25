import aioredis

import settings

redis = aioredis.from_url(settings.REDIS_URL, db=1)
