# Third-party notices

## IqraAI

The initial Quran ASR adapter design was adapted from the MIT-licensed IqraAI project by Abdirahman Ahmed:

https://github.com/AbdirahmanNomad/IqraAI

IqraAI uses the public Hugging Face model `tarteel-ai/whisper-base-ar-quran` through the Transformers automatic-speech-recognition pipeline.

MIT License copyright notice:

Copyright (c) 2025 Abdirahman Ahmed (https://abdirahman.net)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to inclusion of the copyright notice and permission notice.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.


## Quranic Phonemizer

Tahsin Bot uses the MIT-licensed `quranic-phonemizer` package by QUD³ to generate
tajweed-aware expected phoneme sequences and rule metadata for Quran references.

Repository: https://github.com/QUD-Technologies/quranic-phonemizer

Copyright (c) 2025 QUD³

The package is used under the MIT License. The copyright notice and permission
notice must be retained with substantial portions of the software.


## Arabic Wav2Vec2 CTC alignment model

Tahsin Bot uses `jonatasgrosman/wav2vec2-large-xlsr-53-arabic` as an Arabic
CTC acoustic model for forced alignment. The model card publishes it under
the Apache License 2.0. The alignment algorithm in Tahsin Bot is implemented
independently as a standard blank-interleaved CTC Viterbi decoder.
