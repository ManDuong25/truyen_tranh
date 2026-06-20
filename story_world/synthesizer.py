from __future__ import annotations

from .models import EventLogEntry, StoryOutput, StoryParagraph


class StorySynthesizer:
    """Grounded deterministic story projection from committed events."""

    def render_chapter(self, events: tuple[EventLogEntry, ...]) -> StoryOutput:
        conflict_events = [event for event in events if event.event_type == "dialogue_conflict"]
        observation_events = [
            event for event in events if event.event_type == "private_observation"
        ]
        paragraphs: list[StoryParagraph] = []
        if conflict_events:
            first = conflict_events[0]
            paragraphs.append(
                StoryParagraph(
                    text=(
                        "Mưa phủ kín cây cầu cũ. Linh ép Khai nói về đêm cha nàng "
                        "biến mất, còn Khai chỉ trả lời quanh co, như thể mỗi chữ "
                        "đều có thể kéo thêm nguy hiểm đến gần."
                    ),
                    support_event_ids=(first.event_id,),
                )
            )
        if len(conflict_events) >= 3:
            third = conflict_events[2]
            paragraphs.append(
                StoryParagraph(
                    text=(
                        "Khi sức ép dâng lên, Khai thừa nhận lời đồn không kể hết "
                        "sự thật. Nhưng lời thú nhận ấy vẫn chỉ là một khe hở nhỏ, "
                        "không phải cánh cửa Linh cần mở."
                    ),
                    support_event_ids=(third.event_id,),
                )
            )
        if observation_events:
            obs = observation_events[0]
            paragraphs.append(
                StoryParagraph(
                    text=(
                        "Trong bóng mưa, Minh im lặng nghe được sự rạn nứt giữa họ. "
                        "Hắn có thêm đòn bẩy, nhưng chưa chạm tới bí mật thật sự "
                        "đang trói Khai lại."
                    ),
                    support_event_ids=(obs.event_id,),
                )
            )
        if conflict_events:
            last = conflict_events[-1]
            paragraphs.append(
                StoryParagraph(
                    text=(
                        "Đến cuối cuộc đối đầu, Linh không có câu trả lời trọn vẹn. "
                        "Nàng chỉ có thêm nghi ngờ, còn Khai mang thêm một tầng im "
                        "lặng mà cả hai đều biết sẽ không thể giữ mãi."
                    ),
                    support_event_ids=(last.event_id,),
                )
            )
        return StoryOutput(title="Chương 1: Mưa Trên Cầu Cũ", paragraphs=tuple(paragraphs))
