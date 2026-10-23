# Lecture 01 Answers

## Exercises

- Model's answer to the course-specific question (the 3 homework levels; a summary is fine):
- What you noticed when comparing it with the correct meaning in the glossary:
- Token counts you displayed (input / output):

## Homework

- Level attempted: Basic / Implementation / Advanced
- What you did:
- Results:
- Observations and questions:

# Lecture 01 Answers

## Exercises

- **Model's answer:** I asked `gemini-3.5-flash-lite` to name the three homework levels in the AIE2026 course. It couldn't answer and asked me to provide the course material.
- **Correct answer:** Basic, Implementation, and Advanced.
- **Comparison:** The model gave a general response instead of answering this course-specific question. The course material provided the correct levels.
- **Token counts:** 18 input tokens and 85 output tokens.

## Homework

- **Levels attempted:** Basic, Implementation, and Advanced.

### Basic — Model and temperature comparison

I used the question "What is LoRA?" to compare responses at different temperatures with `gemini-3.5-flash-lite`.

| Temperature | Time (seconds) | Input tokens | Output tokens |
|---|---:|---:|---:|
| 0.0 | 11.91 | 6 | 745 |
| 0.7 | 3.60 | 6 | 737 |
| 1.0 | 2.96 | 6 | 720 |

I also ran the same question with two models.

| Model | Time (seconds) | Input tokens | Output tokens |
|---|---:|---:|---:|
| gemini-3.5-flash-lite | 11.91 | 6 | 745 |
| gemini-3.5-flash | 11.87 | 6 | 874 |

The answers were mostly similar. Both explained that LoRA fine-tunes a model by training small low-rank matrices instead of changing all the original model weights. The wording and amount of detail differed. Since these were individual runs, I cannot conclude that temperature alone caused the differences in response time.

### Implementation — Follow-up questions

I modified `app/ask.py` to add a `--chat` option. This lets me ask follow-up questions while keeping the earlier conversation as context.

After asking about LoRA, I asked the model to summarize its previous answer in one sentence. It gave a relevant summary. The follow-up used 698 input tokens and 39 output tokens, and took 8.33 seconds. The input token count was much higher than for the first question because the previous conversation was included.

### Advanced — Timing and token counts

I added response-time and token-count reporting and tested different questions with different models.

For "Define overfitting in two sentences", I got these results:

| Model | Time (seconds) | Input tokens | Output tokens |
|---|---:|---:|---:|
| gemini-3.5-flash-lite | 20.81 | 7 | 49 |
| gemini-3.5-flash | 3.40 | 7 | 52 |

Both answers explained that overfitting happens when a model fits its training data too closely and performs poorly on new data.

One request to `gemini-3.5-flash-lite` failed with a 503 model-busy error. I tried the question again using `gemini-3.5-flash`, and it worked. This showed that model availability can affect experiments. The error alone does not establish that a quota limit was reached.

### Observations and questions

- Changing the temperature did not substantially change the main explanation of LoRA in these runs.
- The two models gave answers of different lengths.
- Response times varied quite a bit. More repeated runs would be needed to compare speed fairly.
- Keeping conversation history made follow-up questions possible, but it also increased input token usage.
- I encountered one 503 error and got a response after switching models.
- All 11 tests passed in an earlier test run; I reran the tests after these final changes to verify the submission.