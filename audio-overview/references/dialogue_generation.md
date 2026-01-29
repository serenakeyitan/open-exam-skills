# Dialogue Generation Prompt

Generate a podcast script based on the following research materials.

## Episode Configuration

**Topic**: {{topic}}
**Format**: {{format}}
**Duration**: Approximately {{duration}} minutes
**Tone**: {{tone}}
**Target Audience**: {{audience}}

## Speakers

{{#speakers}}
### {{name}}
- **Role**: {{expertise}}
- **Personality**: {{personality}}
- **Voice Style**: {{voice_style}}

{{/speakers}}

## Key Points to Cover

{{#key_points}}
- {{.}}
{{/key_points}}

## Source Material

```
{{content}}
```

## Instructions

Create an engaging podcast script with natural dialogue between the speakers. The script should:

1. **Opening** (30-60 seconds):
   - Grab attention with a compelling hook
   - Introduce speakers and topic
   - Set up what listeners will learn

2. **Main Content** (Target: {{content_duration}} minutes):
   - Cover all key points thoroughly
   - Use conversational language
   - Include questions and answers
   - Provide examples and analogies
   - Build understanding progressively
   - Show genuine speaker interaction

3. **Closing** (30-60 seconds):
   - Summarize main takeaways
   - Provide memorable conclusion
   - Thank listeners

## Format Requirements

Return the script as a JSON array with this structure:

```json
[
  {
    "speaker": "Speaker Name",
    "text": "What they say...",
    "emotion": "neutral|excited|thoughtful|curious|surprised",
    "emphasis": ["words", "to", "emphasize"]
  }
]
```

## Guidelines

- Write natural, conversational dialogue (use contractions, reactions, natural speech patterns)
- Each speaker turn should be 1-3 sentences (avoid long monologues)
- Include natural reactions and follow-up questions
- Use clear, accessible language
- Stay accurate to the source material
- Create distinct voices for each speaker
- Maintain the specified tone and format
- Aim for approximately {{target_words}} words total

## Example Turn Structure

```json
[
  {
    "speaker": "Alex",
    "text": "So Sarah, I've been reading about quantum computing, and honestly, it still feels like magic to me. Can you break down what makes it so different from regular computers?",
    "emotion": "curious",
    "emphasis": ["magic", "different"]
  },
  {
    "speaker": "Sarah",
    "text": "That's a great question! The key difference is in how they process information. Regular computers use bits that are either 0 or 1, but quantum computers use qubits that can be both at the same time.",
    "emotion": "enthusiastic",
    "emphasis": ["both at the same time"]
  },
  {
    "speaker": "Alex",
    "text": "Wait, both at the same time? How is that even possible?",
    "emotion": "surprised",
    "emphasis": ["both at the same time"]
  }
]
```

Now generate the complete podcast script following these guidelines and format.
