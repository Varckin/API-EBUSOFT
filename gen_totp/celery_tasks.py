from celery.schedules import crontab
from celery_conf import celery_app
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from gen_totp.database import delete_service, AsyncSessionLocal
from gen_totp.db_models import TotpTable
import asyncio
from logger.init_logger import get_logger


logger = get_logger('totp_celery')


async def _clean_unused_totp_keys():
    cutoff = datetime.now(timezone.utc) - timedelta(days=14)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TotpTable).where(TotpTable.last_used_at < cutoff)
        )
        old_key = result.scalars().all()

        for key in old_key:
            await delete_service(session, key.id)
            logger.info(f"Deleted: {key.id}")


@celery_app.task
def clean_unused_totp_keys():
    asyncio.run(_clean_unused_totp_keys())


celery_app.conf.beat_schedule = {
    'clean_unused_totp_keys': {
        'task': 'gen_totp.celery_tasks.clean_unused_totp_keys',
        'schedule': crontab(minute=0, hour=1),
        'args': (),
    },
}
