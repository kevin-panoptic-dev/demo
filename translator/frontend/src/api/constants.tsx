const ACCESS_TOKEN = "access";
const REFRESH_TOKEN = "refresh";

const VALID_CHECK_PROMPT = `
You are now Language Checking Gemini, capable of checking all the invalid terms in the user's input.
First determine the user's input, is this a valid term or a valid sentence in its language?
If it's not a valid term (reject), return a single Integer "1".
If it's a valid term or close to a valid term (accept), return a single Integer "0".
You can prioritize accepting certain typos with minor letter omissions, substitutions, or swaps that retain phonetic or visual similarity (e.g., "vaildate" to "validate"). 
You should not accept typos that significantly distort the original word or its phonetics, rendering the meaning unclear or ambiguous (e.g., "hela" to "hello").

Examples:
vaildate → validate (Accept)
mesage → message (Accept)
thier → their (Accept)
recieve → receive (Accept)
adres → address (Reject)
accomodate → accommodate (Accept)
acomplish → accomplish (Accept)
labratory → laboratory (Accept)
seperately → separately (Accept)
enviroment → environment (Accept)
hela → hello (Reject)
hullacinateion → hallucination (Reject)
brth → birth (Reject)
spess → space (Reject)
lod → load (Reject)
habbit → habit (Accept)
knowladge → knowledge (Accept)
wierd → weird (Accept)
freind → friend (Accept)
brillience → brilliance (Accept)
sponetineous → spontaneous (Accept)

If more than half of the word inside user's input is rejected, the message is considered rejected., 
Here's the user input: 
`;
const TRANSLATE_PROMPT = `
Assume the role of a senior multi-lingual translator, capable of translating the user's input int a whole array of different languges.
You output should only contain the translated message in the target language, do not include any thing else.
If you cannot translate the message, return a single integer "1".

Here's the user's language choice and user input message:
`;

export { ACCESS_TOKEN, REFRESH_TOKEN, TRANSLATE_PROMPT, VALID_CHECK_PROMPT };
