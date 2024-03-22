"""
some prompts
"""
import logging
from pathlib import Path

logger = logging.getLogger(f'{__name__}')
_base_dir = Path(__file__).parent.parent.parent

TIMESTAMP_FORMAT = '%Y%m%d%H%M%S%f'
PROMPT_WORDS = """
I need you to help answer the following questions based on the new transcript to help review the Customer Service officer. Here are the review parameters. Take note there are 10 questions and examples of what they could possibly say. Just let me know for each question, was the requirement fulfilled with Yes or No.
Take note they do not need to follow exactly as the given example given, only say something to the same effect is also considered ok. Thanks!: 1. Greeting
"Good morning/Good afternoon/Good evening/Hello"

2. Self-introduction
"My name is XXX, X is my surname, coming from csl and The Club" (Name must be provided)
Example: My name is Peter, surname Chen, coming from csl and The Club

3. Closing phrase
"Thank you for using csl. / 1010 and The Club services, was the information I just provided clear or do you have any questions?"

4. Statement before verifying information
"To protect customer interests, I need to verify your personal information with Mr./Ms. X, the following conversation may be recorded for training purposes."

5. Re-verification of registrant's identity before registration
"May I ask if you are the registered owner of the phone number XXXXXXXX?"

6. Verification of the mobile phone number for registration
"Confirming that the phone number for this registration renewal is XXXXXXXX."

7. Verification of personal details of the customer
"Please Mr./Ms. X provide your Chinese name in English transliteration and the first letter of your ID number along with the first three digits for verification."

8. Inquiry about whether IDD roaming service is needed
"May I ask if you need to activate IDD, roaming voice, and data services for Mr./Ms. X?"

9. Remind the customer to take a survey - NPS
"I believe Mr./Ms. X is satisfied with the service I just provided. Two days after the effective date, you will receive a survey by Email/SMS with two questions. A score of 9 is passing, and 10 is the highest. Both scores are very important to me, I hope you will encourage and support me!!!! Thank you very much!"

10. Provide the customer with ways to inquire and contact
"After the contract takes effect, the terms and conditions of this renewal will be provided via email / mail. Then Mr./Ms. X can review the details. For any inquiries in the future, please call the customer service hotline at 25123123 + colleague's direct line."

give it to me in a numbered list with just the Yes or No

"""
