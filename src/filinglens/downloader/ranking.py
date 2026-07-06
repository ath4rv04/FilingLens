class PDFRanker:
    """Intelligent target evaluation filtering outputs matching specific numerical configurations efficiently."""

    @staticmethod
    def score_candidate(url: str, year: str, company: str) -> int:
        score = 0
        target = url.lower()

        # Positive Attributes mapped logically
        if target.endswith(".pdf") or ".pdf?" in target:
            score += 40
        if "annual" in target:
            score += 30
        if "integrated" in target:
            score += 20
        if "report" in target:
            score += 20

        raw_yr = year.replace("FY", "")
        if year.lower() in target or raw_yr in target:
            score += 35

        comp = company.lower().split()[0]
        if comp in target:
            score += 25

        if "investor" in target or "relations" in target or "ir" in target:
            score += 15

        # Negative attributes avoiding fake files mapping targets properly
        if "quarterly" in target or "q1" in target or "q2" in target or "q3" in target:
            score -= 50
        if "presentation" in target:
            score -= 50
        if "earnings" in target or "call" in target:
            score -= 50
        if "transcript" in target:
            score -= 40
        if "sustainability" in target:
            score -= 20
        if "esg" in target:
            score -= 15
        if "press" in target or "release" in target:
            score -= 30

        return score

    @classmethod
    def rank_candidates(
        cls, urls: list[str], year: str, company: str, top_k: int = 5
    ) -> list[tuple[int, str]]:
        """Wraps output arrays checking explicit combinations securely limiting sequences cleanly natively!"""
        ranked = []
        for url in set(urls):
            score = cls.score_candidate(url, year, company)
            if score > 0:
                ranked.append((score, url))

        ranked.sort(key=lambda x: x[0], reverse=True)
        return ranked[:top_k]
