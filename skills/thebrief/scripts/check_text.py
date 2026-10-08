#!/usr/bin/env python3
"""Быстрая проверка русского текста по правилам TheBrief.

Подсвечивает стоп-слова, канцелярит, штампы, ИИ-маркеры и рыночные эмоции,
считает знаки и длину предложений. Это подсказки для редактора, а не приговор:
каждое найденное слово проверь по правилу «стой → думай → режь → наполняй».

Использование:
    python check_text.py текст.md
    python check_text.py текст.md --format telegram
    cat текст.md | python check_text.py - --format onepager
    python check_text.py текст.md --json

Форматы: telegram, onepager, slides, plain (по умолчанию).
"""

import argparse
import json
import re
import sys
import unicodedata

FLAGS = re.IGNORECASE | re.UNICODE

# Категория -> список (регулярное выражение, подсказка)
PATTERNS = {
    "вводные и подводки": [
        (r"\b(стоит|следует|необходимо|важно|нужно) (отметить|подчеркнуть|понимать|учитывать|сказать|заметить)\b", "удалить, мысль сказать сразу"),
        (r"\bкак (известно|мы знаем|правило)\b", "удалить или дать источник"),
        (r"\b(по сути|на самом деле|в принципе|безусловно|разумеется|очевидно|надо сказать|к слову|собственно говоря)\b", "удалить"),
        (r"\bв свою очередь\b", "удалить"),
        (r"\bтаким образом\b", "пустая связка, удалить"),
        (r"\b(в заключение|подводя итог|итак)\b", "пустая концовка"),
    ],
    "паразиты времени": [
        (r"\bв настоящее время\b|\bна сегодняшний день\b|\bна (данный|текущий) момент\b|\bв данный момент\b", "удалить или назвать дату"),
        (r"\bв текущ(их|ей) (условиях|рыночн\w+ (условиях|ситуации)|ситуации)\b|\bв современных реалиях\b|\bна текущем этапе\b", "удалить или назвать период"),
    ],
    "навязанные оценки": [
        (r"\b(выгодн|над[её]жн|удобн|эффективн|оптимальн|качественн|уникальн|инновационн|передов|привлекательн|идеальн|отличн|превосходн|прекрасн)\w*", "заменить фактом"),
        (r"\b(лучш(ий|ая|ее|ие|их|ую|им|ей)|лидер\w*)\b", "сравнение без базы — факт или источник"),
    ],
    "штампы": [
        (r"\bдинамично развива\w+", "что конкретно?"),
        (r"\bширок(ий|ого|им|ом|ая|ую) (спектр|ассортимент|выбор|круг|линейк)\w*", "что конкретно?"),
        (r"\bиндивидуальн\w+ подход\w*|\bклиентоориентированн?\w*", "что конкретно?"),
        (r"\bсинерги\w*|\bэкосистем\w*|\bбесшовн\w*", "операционный факт за словом"),
        (r"\b(качественно )?нов(ый|ого|ом) уровень|\bна новый уровень\b", "что именно изменится?"),
        (r"\bкоманда профессионалов\b|\bмноголетн\w+ опыт\w*|\bвзаимовыгодн\w+|\bкомплексн\w+ решени\w*", "факт вместо штампа"),
        (r"\bне упустите\b|\bуникальн\w+ возможност\w*|\bв кратчайшие сроки\b|\bгибк\w+ услови\w*", "рекламный штамп"),
        (r"\bна фоне\b", "назвать причину или убрать"),
        (r"\bприобрета\w* (всё |все )?(большую )?популярност\w*|\bвс[её] больш\w+ популярност\w*|\bнабира\w* оборот\w*", "газетный штамп — нужна цифра"),
        (r"\bтих(ая|ую) гаван\w*|\bпассивн\w+ доход\w*|\bзаставить деньги работать\b|\bфинансов\w+ свобод\w*", "финансовый штамп"),
        (r"\bбудем рады\b|\bнадеемся на\b|\bплодотворн\w+", "призыв без действия"),
    ],
    "неопределённость": [
        (r"\b(многие|многих|некоторые|некоторых|большинств\w*|множество|целый ряд|ряд (экспертов|аналитиков|компаний|банков|инвесторов))\b", "число или источник"),
        (r"\bэксперт\w*\b", "кто именно?"),
        (r"\bаналитик\w* (счита|ожида|увере|полага|прогнозир)\w*", "кто именно, когда?"),
        (r"\b(зачастую|в ряде случаев|большое количество|значительн\w+ част\w*)\b", "число или условие"),
        (r"\bболее чем\b", "точное число?"),
    ],
    "канцелярит": [
        (r"\bявля(ет|ют|л|ться|ющ|вш)\w*", "«это», «—» или прямой глагол"),
        (r"\bосуществ\w*", "прямой глагол"),
        (r"\bпроизв(од(ит|ят|ится|ятся|ить)|ед(ен|ено|ена|ены|ение|ения))\b", "прямой глагол: «оплатить», «рассчитать»"),
        (r"\bпредставля\w* собой\b", "«это»"),
        (r"\bданн(ый|ая|ое|ые|ого|ой|ому|ым|ых|ыми|ую)\b", "«этот» или убрать"),
        (r"\bв рамках\b|\bв целях\b|\bв связи с\b|\bв условиях\b|\bпосредством\b|\bвышеуказанн\w+|\bнижеследующ\w+|\bсоответствующ\w+|\bтак называем\w+", "простой оборот"),
        (r"\bна \w+ основе\b", "«регулярно», «каждый день»"),
        (r"\bимеет место\b|\bприня\w* участие\b|\bоказ\w* влияние\b|\bнес(ёт|ет|ут) ответственность\b", "глагол"),
    ],
    "слабые глаголы": [
        (r"\bпозвол(яет|яют|ит|ят|ило|ила|ял|яла|ять|яющ)\w*", "прямое действие: «приносит», «можно»"),
        (r"\bспособству\w*", "прямое действие"),
        (r"\bобеспечива\w*", "прямое действие (если не про залог)"),
        (r"\bда(ёт|ет|ют) возможность\b", "«можно»"),
    ],
    "цепочки существительных": [
        (r"\b\w+(ание|ение|ения|ании|ению|ацию|ации|ация|ствие|ствия)\s+\w+(ания|ения|ации|ости|ств|ствия)\b", "вернуть глагол и действующее лицо"),
    ],
    "усилители": [
        (r"\b(очень|крайне|максимально|абсолютно|действительно|по-настоящему|реально|значительно|существенно)\b", "убрать или дать меру"),
        (r"\b(колоссальн|огромн|невероятн|беспрецедентн|максимальн)\w*", "убрать или дать меру"),
        (r"\bсам(ый|ая|ое|ые|ых|ого|ой|ую)\s+\w+(ый|ий|ая|ое|ые|ых|ого|ой|ую)\b", "превосходная степень — нужна база"),
    ],
    "страдательный залог": [
        (r"\b(был|была|было|были|будет|будут)\s+\w+(ен|ена|ено|ены|ан|ана|ано|аны|ят|ята|ято|яты)\b", "кто сделал?"),
        (r"\bбыло принято решение\b", "кто решил?"),
    ],
    "местоимения": [
        (r"\bсво(й|его|ему|им|ём|ем|я|ю|ей|е|и|их|ими)\b", "без «свой» понятно?"),
        (r"\bвы можете\b", "«можно» или прямое действие"),
    ],
    "кальки": [
        (r"\bигра\w* (\w+ )?роль\b", "«от … зависит»"),
        (r"\bимеет смысл\b|\bв терминах\b|\bфокус на\b|\bэто про\b", "русский оборот"),
        (r"\b(кейс|инсайт|драйвер)\w*", "«случай», «вывод», «причина роста»"),
    ],
    "ИИ-маркеры": [
        (r"\bне просто\b", "ложное противопоставление — сказать прямо"),
        (r"\bне только\b[^.!?]*\bно и\b", "«не только…, но и…» — проверить, есть ли контраст"),
        (r"\bдавайте\b|\bразбер[её]мся\b|\bрассмотрим\b", "подводка — начать с сути"),
        (r"\bв этом (посте|тексте|материале|обзоре)\b", "анонс вместо содержания"),
        (r"\bпочему это важно\b|\bвс[её] просто\b|\bзвучит сложно\b", "риторическая подводка"),
        (r"\bоткрыва\w* (нов\w+ )?(возможност|горизонт)\w*|\bв современном мире\b|\bнов(ая|ую) эр\w*|\bключев\w+ рол\w*", "пафос"),
        (r"\bконечно!|\bотличный вопрос\b|\bнадеюсь, это поможет\b|\bвот (ваш|готовый) текст\b", "реплика ассистента"),
        (r"\bдрузья\b|\bребята\b", "панибратство"),
        (r"\bуспейте\b|\bпока не поздно\b|\bуже сегодня\b", "давление срочностью"),
    ],
    "рыночные эмоции": [
        (r"\bобвал\w*|\bрухн\w*|\bвзл[её]т\w*|\bулетел\w*|\bракет\w*|\bпаник\w*|\bштормит\b|\bкровав\w*|\bна хаях\b|\bпамп\w*", "событие и масштаб вместо эмоции"),
    ],
}

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF\U00002B00-\U00002BFF\U0001F900-\U0001F9FF]",
    re.UNICODE,
)
FACT_RE = re.compile(r"\[нужен факт[^\]]*\]", FLAGS)
SENT_SPLIT_RE = re.compile(r"(?<=[.!?…])\s+(?=[«\"(\[A-ZА-ЯЁ0-9—–-])")

LIMITS = {
    "telegram": (1200, 2000, 3500),
    "onepager": (1500, 2500, 3000),
    "plain": (None, None, None),
    "slides": (None, None, None),
}


def strip_markdown(text: str) -> str:
    text = re.sub(r"^>[ \t]?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*|__|(?<!\w)_(?!\s)|(?<!\s)_(?!\w)", "", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    return text


def find_hits(text: str):
    hits = []
    lines = text.splitlines()
    for category, patterns in PATTERNS.items():
        for pattern, hint in patterns:
            rx = re.compile(pattern, FLAGS)
            for line_no, line in enumerate(lines, 1):
                clean = FACT_RE.sub("", line)
                for m in rx.finditer(clean):
                    start = max(0, m.start() - 30)
                    end = min(len(clean), m.end() + 30)
                    hits.append({
                        "category": category,
                        "match": m.group(0),
                        "line": line_no,
                        "context": clean[start:end].strip(),
                        "hint": hint,
                    })
    return hits


def sentences(text: str):
    body = FACT_RE.sub("", text)
    parts = []
    for para in re.split(r"\n\s*\n|\n(?=[—–•\-*]\s|\d+[.)]\s)", body):
        para = " ".join(para.split())
        if not para:
            continue
        parts.extend(s for s in SENT_SPLIT_RE.split(para) if s.strip())
    return parts


def word_count(s: str) -> int:
    return len(re.findall(r"[\wёЁ]+(?:-[\wёЁ]+)*", s))


def slide_blocks(text: str):
    blocks = re.split(r"(?=^\s*\**\s*Слайд\s*\d+)", text, flags=re.MULTILINE | re.IGNORECASE)
    result = []
    for b in blocks:
        b = b.strip()
        if not re.match(r"\**\s*Слайд\s*\d+", b, flags=re.IGNORECASE):
            continue
        first, _, rest = b.partition("\n")
        rest = re.split(r"_?Для спикера", rest, flags=re.IGNORECASE)[0]
        result.append({"title": first.strip("* ").strip(), "body_words": word_count(rest)})
    return result


def analyze(raw: str, fmt: str):
    text = strip_markdown(raw)
    chars = len(text.strip())
    chars_no_spaces = len(re.sub(r"\s", "", text))
    sents = sentences(text)
    lengths = [word_count(s) for s in sents]
    long_sents = [s for s, n in zip(sents, lengths) if n > 25]
    hits = find_hits(text)
    emoji = EMOJI_RE.findall(raw)
    fact_marks = FACT_RE.findall(raw)
    numbers = [int(n) for n in re.findall(r"\[нужен факт\s*(\d+)", raw, FLAGS)]
    report = {
        "format": fmt,
        "chars": chars,
        "chars_no_spaces": chars_no_spaces,
        "words": word_count(text),
        "sentences": len(sents),
        "avg_sentence_words": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "long_sentences": long_sents[:5],
        "long_sentences_count": len(long_sents),
        "exclamations": raw.count("!"),
        "emoji": len(emoji),
        "straight_quotes": len(re.findall(r"\"[^\"\n]+\"", raw)),
        "hyphen_as_dash": len(re.findall(r"\s-\s", raw)),
        "markdown_headings": len(re.findall(r"^#+\s", raw, flags=re.MULTILINE)),
        "markdown_tables": len(re.findall(r"^\s*\|.*\|\s*$", raw, flags=re.MULTILINE)),
        "fact_marks": len(fact_marks),
        "fact_numbers": numbers,
        "hits": hits,
    }
    lo, hi, hard = LIMITS.get(fmt, (None, None, None))
    report["length_note"] = None
    if lo and chars < lo:
        report["length_note"] = f"короче обычного: {chars} знаков при норме {lo}–{hi}"
    elif hi and chars > hard:
        report["length_note"] = f"длиннее предела: {chars} знаков при пределе {hard}"
    elif hi and chars > hi:
        report["length_note"] = f"длиннее обычного: {chars} знаков при норме {lo}–{hi} (допустимо до {hard} для разбора)"
    if fmt == "slides":
        report["slides"] = slide_blocks(raw)
    return report


def print_report(r):
    out = []
    out.append(f"Формат: {r['format']}")
    out.append(f"Знаков с пробелами: {r['chars']}, без пробелов: {r['chars_no_spaces']}, слов: {r['words']}")
    if r["length_note"]:
        out.append(f"Длина: {r['length_note']}")
    out.append(f"Предложений: {r['sentences']}, в среднем {r['avg_sentence_words']} слов")
    if r["long_sentences_count"]:
        out.append(f"Длинных предложений (>25 слов): {r['long_sentences_count']}")
        for s in r["long_sentences"]:
            out.append(f"  — {s[:140]}{'…' if len(s) > 140 else ''}")
    for key, label in [("exclamations", "Восклицательных знаков"), ("emoji", "Эмодзи"),
                       ("straight_quotes", "Прямых кавычек вместо «ёлочек»"),
                       ("hyphen_as_dash", "Дефисов вместо тире"),
                       ("markdown_headings", "Markdown-заголовков (#)"),
                       ("markdown_tables", "Строк таблиц")]:
        if r[key]:
            out.append(f"{label}: {r[key]}")
    if r["fact_marks"]:
        out.append(f"Меток [нужен факт]: {r['fact_marks']}")
        nums = r["fact_numbers"]
        if nums and sorted(set(nums)) != list(range(1, max(nums) + 1)):
            out.append(f"  Нумерация меток с пропусками: {sorted(set(nums))}")
    if r.get("slides"):
        out.append("Слайды:")
        for s in r["slides"]:
            flag = "  ← много текста" if s["body_words"] > 45 else ""
            out.append(f"  {s['title'][:70]} — {s['body_words']} слов{flag}")
    if r["hits"]:
        out.append("")
        out.append("Проверь (стой → думай → режь → наполняй):")
        by_cat = {}
        for h in r["hits"]:
            by_cat.setdefault(h["category"], []).append(h)
        for cat, items in by_cat.items():
            out.append(f"• {cat}: {len(items)}")
            for h in items[:8]:
                out.append(f"    стр. {h['line']}: «{h['match']}» — {h['hint']} | …{h['context']}…")
            if len(items) > 8:
                out.append(f"    … и ещё {len(items) - 8}")
    else:
        out.append("Стоп-слов и ИИ-маркеров из списка не найдено.")
    print("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description="Проверка текста по правилам TheBrief")
    ap.add_argument("path", help="файл с текстом или - для stdin")
    ap.add_argument("--format", default="plain", choices=sorted(LIMITS))
    ap.add_argument("--json", action="store_true", help="вывести результат в JSON")
    args = ap.parse_args()
    raw = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    raw = unicodedata.normalize("NFC", raw)
    report = analyze(raw, args.format)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
