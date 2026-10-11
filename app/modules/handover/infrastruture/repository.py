from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.handover.domain.models import AudioRecord, AudioTranscriptSegment


class HandoverRepository:
    """SQLAlchemy persistence adapter used by handover application services."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_audio(self, audio_id: UUID) -> AudioRecord | None:
        return await self.session.get(AudioRecord, audio_id)

    async def list_segments(self, version_id: UUID) -> list[AudioTranscriptSegment]:
        rows = await self.session.scalars(
            select(AudioTranscriptSegment)
            .where(AudioTranscriptSegment.transcript_version_id == version_id)
            .order_by(AudioTranscriptSegment.segment_index)
        )
        return list(rows)