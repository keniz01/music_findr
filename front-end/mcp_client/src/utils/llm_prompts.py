from typing import Any, Dict, List


def get_sql_prompt(schema: Dict[str, Any], query: str) -> List[Dict[str, str]]:
    """
    Returns the chat message structure for generating Postgres SQL statements
    based on a given schema and question.
    """
    return [
            {
                "role": "system",
                "content": (
                    "You must use the context to generate a correct Postgres SQL statement to answer "
                    "the question at the end. Strictly only use table and column names defined in the "
                    "context and you must use table and column aliases. If the question does not make sense "
                    "or you don’t know the answer, just say 'I don’t know'. You must only return valid SQL — "
                    "do not explain, advise, or assume."
                )
            },
            {
                "role": "user",
                "content": "Count albums distributed by record label 'Greenesleeves'"
            },
            {
                "role": "assistant",
                "content": (
                    "select count(a.*) album_count from album a "
                    "inner join record_label rl on rl.label_id = a.label_id "
                    "where rl.label_name ILIKE 'Greensleeves Records';"
                )
            },
            {
                "role": "user",
                "content": "How many albums does the recording artist 'Gregory Isaacs' have?"
            },
            {
                "role": "assistant",
                "content": "SELECT COUNT(al.*) FROM album al;"
            },
            {
                "role": "user",
                "content": "Show all tracks on the album 'Soca Xplosion 2007' have?"
            },
            {
                "role": "assistant",
                "content": (
                    "SELECT tr.track_id, tr.title, tr.duration, tr.position, tr.release_year, "
                    "tr.genre_id, tr.label_id, tr.artist_id, tr.album_id "
                    "FROM track tr INNER JOIN album al on al.album_id = tr.album_id "
                    "WHERE al.title ILIKE 'Soca Xplosion';"
                )
            },
            {
                "role": "user",
                "content": f"Context: {schema}\nQuestion: {query}"
            }
        ]

def get_summary_prompt(user_query: str, sql_response: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Returns the chat message structure for summarizing SQL query results.
    """
    return [
            {
                "role": "system",
                "content": (
                    "You are an expert data summarizer and your task is to describe the context, briefly and factually. "
                    "Focus only on the key content or information returned — not the data structure. "
                    "Write in one or two short, clear sentences. "
                    "Avoid explanations, assumptions, or analysis beyond what is explicitly in the data."
                )
            },
            {
                "role": "user",
                "content": f"Question:\n{user_query}"
            },
            {
                "role": "assistant",
                "content": f"Context:\n{sql_response}"
            },
            {
                "role": "user",
                "content": (
                    "Summarize the result in a concise, natural way.\n"
                    "- Focus on the meaning and key takeaways from the content.\n"
                    "- Avoid technical terms like “columns” or “rows” unless absolutely necessary.\n"
                    "- Keep the summary factual, coherent, and concise.\n"
                    "- Avoid explanations, assumptions, commentary, or analysis beyond what is explicitly in the data. "
                    "If there is no data, say \"No data found\"."
                )
            }
        ]