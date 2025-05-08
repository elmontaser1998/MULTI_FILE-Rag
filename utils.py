import os
import pandas as pd
from io import StringIO


def save_chat_to_csv(chat_history):
    df = pd.DataFrame(chat_history)
    csv = StringIO()
    df.to_csv(csv, index=False)
    csv.seek(0)
    return csv.getvalue()
