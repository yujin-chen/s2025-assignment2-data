#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[2]
sys.path.append(str(CURRENT_FILE))
import random
from warcio.archiveiterator import ArchiveIterator
from cs336_data.extract_text import extract_text_from_html_bytes
from cs336_data.identity_language import identify_language
from cs336_data.problem_experiment.common import KOA_SCRATCH_PATH

WARC_FILE_PATH = KOA_SCRATCH_PATH / "CC-MAIN-20180420081400-20180420101400-00118.warc.gz"

def extract_texts_from_warc(warc_path, num_samples=20):

    extracted_texts = []
    
    with open(warc_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == "response":
                raw_html = record.content_stream().read()
                extracted_text = extract_text_from_html_bytes(raw_html)
                if extracted_text.strip():
                    extracted_texts.append(extracted_text)

    sampled_texts = random.sample(extracted_texts, min(num_samples, len(extracted_texts)))
    return sampled_texts

def evaluate_language_identification(warc_path):

    texts = extract_texts_from_warc(warc_path)
    
    results = []
    for i, text in enumerate(texts):
        predicted_lang, confidence = identify_language(text)
        
        print(f"Sample {i+1}:")
        print(f"Extracted Text: {text[:600]}...")  # Show only the first 300 characters
        print(f"Predicted Language: {predicted_lang} (Confidence: {confidence:.2f})")
        
        # Manually label the language
        actual_lang = input("Enter actual language (e.g., 'en' for English, 'fr' for French): ").strip()
        
        # Store results
        results.append({
            "text": text[:600],  # Store only a preview for analysis since just for language identification
            "predicted_lang": predicted_lang,
            "actual_lang": actual_lang,
            "confidence": confidence
        })
    
    return results

# Run evaluation
language_results = evaluate_language_identification(WARC_FILE_PATH)

# Analyze results
total_samples = len(language_results)
correct_predictions = sum(1 for r in language_results if r["predicted_lang"] == r["actual_lang"])
english_samples = sum(1 for r in language_results if r["actual_lang"] == "en")

accuracy = correct_predictions / total_samples
english_fraction = english_samples / total_samples

print("\n=== Evaluation Results ===")
print(f"Total Samples: {total_samples}")
print(f"Correct Predictions: {correct_predictions} ({accuracy:.2%})")
print(f"English Documents: {english_samples} ({english_fraction:.2%})")

# Determine suitable confidence threshold
confidences = [r["confidence"] for r in language_results if r["predicted_lang"] == r["actual_lang"]]
avg_confidence = sum(confidences) / len(confidences) if confidences else 0
print(f"Recommended Confidence Threshold: {avg_confidence:.2f}")

#RUN RESULT. Problem (language_identification) (c)
'''
Sample 1:
Extracted Text: Butterfly & Nature Photography by Silvia Reiche
  • Home
    • Update News
  • About
    • Biography
    • Photography
    • Workshops
    • Contact
  • Blog
  • Butterfly Gallery
    • Hesperiidae >
      • Chequered Skipper
      • Dingy Skipper
      • Essex Skipper
      • Grizzled Skipper
     ...
Predicted Language: en (Confidence: 0.53)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 2:
Extracted Text: Bar Of Western Store

Western Furniture, Decor & Apparel in Clinton, AR

Menu

Skip to content
  • Welcome!
  • Shop Furniture
    • Sofas & Chairs
    • Tables
    • Kitchen & Dining
    • Bedroom
    • Bathroom
    • Lighting/Décor
  • Chuckwagon Races
  • Directions

cropped-Bar-Of-Store-Banner-7...
Predicted Language: en (Confidence: 0.67)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 3:
Extracted Text:   • Title list
  • Login

マンチカン虎麦＆ほたる、時々虎鉄をよろしく！

愛猫を亡くしたママが兄妹猫をお迎えしドタバタな毎日。

  • Twitter
  • Facebook
  • RSSフィード
14 2016

コロナウイルス退治しました！

２月11日の祝日にやっと消毒をする決断をしたkotetsuママ(*￣Oﾉ￣*)ﾎｰｯﾎｯﾎ!!
朝から夕方まで１日かかりで我が家からコロナウイルスを退治しました((((ToT)†~~~ 悪霊退散!!!

虎鉄の使っていたおもちゃは除菌、洗浄出来ないものは全て捨てました(　；∀；) ｶﾅｼｲﾅｰ
一番辛かったのは、虎鉄が...
Predicted Language: ja (Confidence: 1.00)
Enter actual language (e.g., 'en' for English, 'fr' for French): ja
Sample 4:
Extracted Text: Acacia Consulting & Research

  • profile
  • people
  • services
  • projects
  • clients
  • contact

barcelona balconiesProfile

Acacia Consulting & Research (ACR) is
an Ottawa, Canada-based company established in 1999. ACR helps municipalities and community-based organizations make better use of...
Predicted Language: en (Confidence: 0.91)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 5:
Extracted Text: Facebook Instagram Google+ YouTube Blog Zdjęcie Wideo Cennik
Hotel Družba
  • Hotel
  • Zakwaterowanie
  • Gastronomia
  • Wellness
  • Kongresy
  • Rodzinny urlop
  • Co robić w Jasnej
    • pl
    • sk
    • ru
    • en
Online booking
    • pl
    • sk
    • ru
    • en
Menu
+
Online booking
  • W...
Predicted Language: pl (Confidence: 0.78)
Enter actual language (e.g., 'en' for English, 'fr' for French): pl
Sample 6:
Extracted Text: Verwendung von Cookies
Wir verwenden eigene Cookies und Cookies von dritten um ein einfacheres Navigieren und einen besseren Service zu ermöglichen. Sollten Sie weiter auf unseren Seiten surfen verstehen wir dies als Einverständniserklärung mit unseren Richtlinien zur Benutzung von Cookies
Der Laden...
Predicted Language: de (Confidence: 0.94)
Enter actual language (e.g., 'en' for English, 'fr' for French): de
Sample 7:
Extracted Text:  "Decorative Home Accessories"
Beautiful objects for home and garden
                                                                  
  • Home
  • FURNITURE
  • GARDEN
  • KITCHEN & HOME
  • LOVELY BITS
  • RETRO
  • LIGHTING
  • MIRRORS & WALL ART
  • ORIGINAL ART BY DAN STIRLING
  • Pet Care
  •...
Predicted Language: en (Confidence: 0.67)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 8:
Extracted Text: Welcome to
the forums at bobdunsire.com
bobdunsire.com | Bagpipe Web Directory | PPOD | Forum Rules | Forum FAQ | Advertising
bobdunsire.com forums bobdunsire.com forums
You can reset your password by going here. Be sure to try your current email and any email addresses you may have had in the past....
Predicted Language: en (Confidence: 0.89)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 9:
Extracted Text: turning pages

29 juni 2012

Vintage sewing material



I just love vintage sewing material, too bad it's rather expensive at flea markets... The needle book, for instance was 8 euros. In perfect condition though. The vendor had lots more fantastic ones, I might go back to purchase one or two to sta...
Predicted Language: en (Confidence: 0.42)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 10:
Extracted Text: Christopher Allis
  • Home
  • Sound
  • Vision
  • Calendar
  • Blog
  • Gear
  • Bio
  • Feedback
  • Contact

Blog Archives

11 Nov '10

Music is the best. FZ

11/11/2010 | Comments: 0 | Posted by: christopherallis | In: What's Spinning?

10998041_10205713277008214_7166135603090461242_nThanks to ...
Predicted Language: en (Confidence: 0.80)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 11:
Extracted Text: Rogers Media uses cookies for personalization, to customize its online advertisements, and for other purposes. Learn more or change your cookie preferences. Rogers Media supports the Digital Advertising Alliance principles. By continuing to use our service, you agree to our use of cookies.
We use co...
Predicted Language: en (Confidence: 0.82)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 12:
Extracted Text: ×

Приглашаем к сотрудничеству поставщиков товаров для дома (посуда, текстиль, сувениры и пр.)

Вопросы и предложения присылайте через форму: заполнить форму
Вакансии Наши магазины Оплата и доставка Гарантия Отправить жалобу Вход / Регистрация
X

Предложите свою цену:

НАЙДИТЕ
цену ниже
ОТПРАВЬТЕ
на...
Predicted Language: ru (Confidence: 0.99)
Enter actual language (e.g., 'en' for English, 'fr' for French): ru
Sample 13:
Extracted Text: Загрузка...
Ваш регион Не указан
Реклама на портале
Вход Регистрация
Мы в социальныхсоц. сетях
Вконтакте Одноклассники Фейсбук Твиттер Инстаграм
  • Одноклассники
  • Твиттер
  • Мы в YouTube
  • Мы в Google+
  • Мы в Vimeo
Свадебный портал. 71
Каталог
Галереи
Статьи
Свадебный сайт
  • Все компании
...
Predicted Language: ru (Confidence: 0.99)
Enter actual language (e.g., 'en' for English, 'fr' for French): ru
Sample 14:
Extracted Text:   • Quick Links
    • Career
    • Betipadhao
    • Grievance Cell
  • Webmail
  • Career
  • Online Payment
  • Admission Open
logo
  • Home
  • About
    • Overview
    • Chairman's Message
    • Director's Message
    • Vice President's Message
    • ADAF's Message
    • Awards & Achivements
  • ...
Predicted Language: en (Confidence: 0.70)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 15:
Extracted Text: Skip to content
Pantone 4C

Pantone 4C

Jeg elsker bare at blogge

  • Home
  • Links
  • Sitemap
  • Blog
Posted on April 11, 2018 by admin

Use These Tips To Have Fun With Your Blog

Many times a blog will focus on one topic. If you are passionate enough to write a blog about one topic, then this ...
Predicted Language: en (Confidence: 0.94)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 16:
Extracted Text: ITライフハック

ブログメディア

ビジネス塾

  • 次の15件 >
2014年07月11日09:00

見えてきた米国の「出口」 10年以上の「徐行運転」？【ビジネス塾】

カテゴリ
経済総合
米国の中央銀行機能を果たす連邦準備理事会（FRB）は、6月に開いた連邦公開市場委員会（FOMC）の議事要旨を公表した。それによれば、市場関係者の予想通り、現在行われている量的緩和（QE3）は10月のFOMCで終了を決める予定のようだ。

以前も述べたが、その後もゼロ金利が続くというのがおおかたの予想だ。ただ、米国経済の好調を背景に、「早期利上げ」の観測も強まっている。円ドル相場や日本の株式市場に...
Predicted Language: ja (Confidence: 1.00)
Enter actual language (e.g., 'en' for English, 'fr' for French): ja
Sample 17:
Extracted Text: US: +1 (707) 877-4321 FR: +33 977-198-888

English Français Deutsch Italiano Español Русский 中国 Português 日本

お気に入り マイカート

燭台、ベアリングエンジェル, テラコッタ バイ Luca Della Robbia (1399-1482, Italy)
3プリントを購入してまで取得 12% + 15%
あなたのカートは、サイト全体すべて12%オフ まで有効:19/04/2018

送料無料となります。返品無料 すべての時間。詳細を参照してください。

燭台、ベアリングエンジェル

...
Predicted Language: ja (Confidence: 0.96)
Enter actual language (e.g., 'en' for English, 'fr' for French): ja
Sample 18:
Extracted Text: Меню
  • Главная
  • О компании
  • Скидки
  • Доставка и оплата
  • Сотрудничество
  • Контакты
Регистрация Вход
0
0.00 руб.
Оформить заказ
Корзина
0 шт.
0.00 руб.
Оформить заказ
официальный дилер продукции ЕВРОПЛАСТ
Планета декора
Лепнина ЕВРОПЛАСТ
с 9-00 до 17-00
+7 (499) 755-52-27
круглосуточно
...
Predicted Language: ru (Confidence: 0.98)
Enter actual language (e.g., 'en' for English, 'fr' for French): ru
Sample 19:
Extracted Text: Back To Bionic

Do you remember the future?
  • BLOG
  • / Music
    • Cold Wave – Dark Electro
    • Detroit Techno
    • Electro
    • Electro Bass / Breaks – EBM
    • Electro Funk / Rap – Funk
    • Electronica – IDM
    • Electropop – Synthpop
    • Funktronica
    • Future Garage – UKG
    • G...
Predicted Language: en (Confidence: 0.61)
Enter actual language (e.g., 'en' for English, 'fr' for French): en
Sample 20:
Extracted Text: ғąѕнιoŋ ﮐ℮cr℮тѕ

  • HOME
  • Review Policy
  • Feed Syndication

Lucia

Posted by ѕtepнanιe on 03/05/2013
Posted in: Uncategorized. Tagged: 7891, BenS Beauty, Maxi Gossamer, PiCHi, Pure Poison, SHOCK, [e], {.essences.}, {{BSD Desing Studio}}. Leave a comment

PNK

 

 

BODY

Skin: Essences – Opera...
Predicted Language: en (Confidence: 0.75)
Enter actual language (e.g., 'en' for English, 'fr' for French): en

=== Evaluation Results ===
Total Samples: 20
Correct Predictions: 20 (100.00%)
English Documents: 12 (60.00%)
Recommended Confidence Threshold: 0.82
'''