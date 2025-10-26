def interval_overlap(start1: int, end1: int, start2: int, end2: int) -> bool:
    return (start1 < end2 and start2 < end1) or (start2 < end1 and start1 < end2)
