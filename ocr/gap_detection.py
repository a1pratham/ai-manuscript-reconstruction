def detect_gaps(df, char_threshold=70, word_threshold=40):

    result = []

    prev_right = None
    prev_line = None

    for _, row in df.iterrows():

        word = str(row["text"])
        conf = float(row["conf"])

        left = int(row["left"])
        width = int(row["width"])
        line = int(row["line_id"])

        # detect new line
        if prev_line is not None and line != prev_line:
            result.append("\n")
            prev_right = None

        # horizontal gap detection
        if prev_right is not None:

            gap = left - prev_right

            if gap > 80:
                result.append("[WORD_GAP]")

        # confidence gaps
        if conf < word_threshold:
            result.append("[WORD_GAP]")

        elif conf < char_threshold:
            result.append(word[:-1] + "[CHAR_GAP]")

        else:
            result.append(word)

        prev_right = left + width
        prev_line = line

    return " ".join(result)