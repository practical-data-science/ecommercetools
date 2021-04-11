import pandas as pd
from transformers import pipeline


def get_summary(text,
                min_length=50,
                max_length=100,
                do_sample=False):
    """Return a summary from a piece of text using a transformer model.

    Args:
        text (string): String of text to summarize. Will be truncated to first 1024 characters.
        min_length (int): Minimum length to return.
        max_length (int): Maximum length to return.
        do_sample (optional, boolean): Set to False to generate unique text or True to extract excerpts.

    Returns:
        string: Summarized text.
    """

    summarizer = pipeline("summarization")
    summary = summarizer(text[:1024],
                         min_length=min_length,
                         max_length=max_length,
                         do_sample=do_sample)
    summary_text = summary[0]['summary_text'].strip().replace(' .', '.')

    return summary_text


def get_summaries(df,
                  text_column,
                  summary_column_name='summary',
                  min_length=50,
                  max_length=100,
                  do_sample=False):
    """Return a summary each of a specified dataframe column using a transformer model.

    Args:
        df (dataframe): Pandas dataframe containing the text to summarize.
        text_column (string): Name of text column to summarize. Will be truncated to first 1024 characters.
        summary_column_name (string, optional): Name of summary column.
        min_length (int, optional): Minimum length to return.
        max_length (int, optional): Maximum length to return.
        do_sample (boolean, optional): Set to False to generate unique text or True to extract excerpts.

    Returns:
        df['summary']: Original dataframe with additional column containing summaries.
    """

    df[summary_column_name] = df.apply(lambda x: get_summary(x[text_column],
                                                             min_length=min_length,
                                                             max_length=max_length,
                                                             do_sample=do_sample), axis=1)
    return df
