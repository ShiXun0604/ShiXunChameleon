def split_string(s: str, n: int) -> list[str]:
    # By chatGPT
    length = len(s)
    chunk_size = length // n
    remainder = length % n

    chunks = []
    start = 0

    for i in range(n):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(s[start:end])
        start = end

    return chunks