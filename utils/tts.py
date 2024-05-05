import os

import torch
import torchaudio


def load_data(audio_folder):
    audios = []
    texts = []
    for audio_file in os.listdir(audio_folder):
        if audio_file.endswith('.wav'):
            audio_path = os.path.join(audio_folder, audio_file)
            waveform, sample_rate = torchaudio.load(audio_path)
            text_path = audio_path.replace('.wav', '.txt')
            with open(text_path) as f:
                text = f.read().strip()
            audios.append((waveform, sample_rate))
            texts.append(text)
    return audios, texts


def train(model, audios, texts, epochs=3, learning_rate=1e-4):
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = torch.nn.MSELoss()  # Вам нужно будет настроить эту функцию под вашу задачу

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for waveform, text in zip(audios, texts):
            optimizer.zero_grad()
            # Предполагается, что модель принимает текст и возвращает аудио
            predicted_waveform = model(text)
            loss = criterion(predicted_waveform, waveform)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        average_loss = total_loss / len(audios)
        print(f'Epoch {epoch + 1}: Average Loss = {average_loss}')


def main():
    model_path = 'data/v4_ru.pt'
    model = torch.load(model_path)
    model.eval()
    audio_folder = 'wav_files'
    audios, texts = load_data(audio_folder)
    train(model, audios, texts)
    torch.save(model.state_dict(), 'fine_tuned_model.pth')
    model.eval()
    sample_text = "Пример текста для синтеза."
    with torch.no_grad():
        generated_waveform = model(sample_text)
        torchaudio.save('output_audio.wav', generated_waveform, 16000)


if __name__ == '__main__':
    main()
