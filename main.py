import requests, json, random, telebot, copy

from NeuralNetwork import NeuralNetwork

TOKEN = "1020169473:AAGJK3HfU1A28nSk4ShASUZ2rMZZBgTGtIU"
API_KEY = "trnsl.1.1.20200308T151048Z.03d1373bdeafd8cd.b5c8fbb1e018b6a093a8fadae53642713cffe3d5"

bot = telebot.TeleBot(TOKEN)

print("Bot has been launched.")

neuralNetwork = NeuralNetwork(4, "data/words.txt", 1000, toLoad=True, name_savedNetwork="saved_networks/network_8_3_2020")
# neuralNetwork = NeuralNetwork(4, "data/words.txt", 1000, toSave=True)
# neuralNetwork.Train()

@bot.message_handler(commands = ['start'])
def startMessage(message):
    bot.send_message(message.chat.id, "Hello, you've sent me /start")

@bot.message_handler(commands = ['tr_generate'])
def answer(message):
    words = []

    for i in range(random.randint(3, 7)):
        words.append(neuralNetwork.Run())

    FROM_LANG = ["sr", "mn", "tg", "tt", "sl", "sk", "ro"]

    to_lang = "ru"

    words_copy = copy.copy(words)

    for lang in FROM_LANG:
        print(lang)

        for wordIndex in range(len(words_copy)):
            if (words_copy[wordIndex] != words[wordIndex]): continue
            response = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate?key=" + API_KEY + "&lang=" + lang + "-" + to_lang + "&text=" + words_copy[wordIndex])

            result = json.loads(response.text)['text'][0]

            print(result)

            if (result != words_copy[wordIndex]): words_copy[wordIndex] = result

    print(" ".join(words_copy))

    bot.send_message(message.chat.id, " ".join(words_copy))

bot.polling()