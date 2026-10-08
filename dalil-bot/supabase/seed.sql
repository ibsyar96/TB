-- EzTajwid data export: 51 reviewed records from original project.
-- Execute in NEW EzTajwid project AFTER schema.sql.
BEGIN;
INSERT INTO public.dalil_tajwid_entries (slug,category,topic,aliases,source_title,source_author,source_verse,arabic_text,meaning_ms,source_url,verification_status) VALUES
('makhraj-17','makhraj','Bilangan 17 makhraj',ARRAY['17 makhraj','jumlah makhraj','مخارج الحروف']::text[],'المقدمة الجزرية','الإمام ابن الجزري','9','مَخَارِجُ الْحُرُوفِ سَبْعَةَ عَشَرْ
عَلَى الَّذِي يَخْتَارُهُ مَنِ اخْتَبَرْ','Makhraj huruf berjumlah tujuh belas menurut pendapat pilihan ulama yang menelitinya.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-dhad','makhraj','Makhraj dhad (ض)',ARRAY['ض','dhad','dad','tepi lidah','حافة اللسان']::text[],'المقدمة الجزرية','الإمام ابن الجزري','13–14','وَالضَّادُ: مِنْ حَافَتِهِ إِذْ وَلِيَا
لَاضْرَاسَ مِنْ أَيْسَرَ أَوْ يُمْنَاهَا','Dhad keluar daripada sisi lidah yang bersentuhan dengan gigi geraham, sama ada sisi kiri atau kanan.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-fa','makhraj','Makhraj fa (ف)',ARRAY['ف','fa','bibir','gigi atas']::text[],'المقدمة الجزرية','الإمام ابن الجزري','18 (petikan)','وَمِنْ بَطْنِ الشَّفَهْ
فَالْفَا مَعَ أَطْرَافِ الثَّنَايَا الْمُشْرِفَهْ','Fa keluar daripada bahagian dalam bibir bawah bersama hujung gigi kacip atas.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-ghain-kha','makhraj','Al-Halq: bahagian terdekat mulut',ARRAY['غ','خ','ghain','kha','tekak bawah']::text[],'المقدمة الجزرية','الإمام ابن الجزري','12 (bahagian pertama)','أَدْنَاهُ غَيْنٌ خَاؤُهَا','Daripada bahagian tekak yang paling dekat dengan mulut keluar ghain (غ) dan kha (خ).','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-halq','makhraj','Al-Halq: pangkal dan tengah tekak',ARRAY['halq','tekak','ء','ه','ع','ح','الحلق']::text[],'المقدمة الجزرية','الإمام ابن الجزري','11','ثُمَّ لِأَقْصَى الْحَلْقِ هَمْزٌ هَاءُ
ثُمَّ لِوَسْطِهِ فَعَيْنٌ حَاءُ','Daripada pangkal tekak keluar hamzah dan ha (ه); daripada tengah tekak keluar ‘ain dan ha (ح).','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-jauf','makhraj','Al-Jauf (rongga)',ARRAY['jauf','rongga','huruf mad','الجوف']::text[],'المقدمة الجزرية','الإمام ابن الجزري','10','فَأَلِفُ الْجَوْفِ وَأُخْتَاهَا وَهِي
حُرُوفُ مَدٍّ لِلْهَوَاءِ تَنْتَهِي','Alif mad dan dua huruf mad yang sejenis dengannya keluar melalui rongga (al-jauf); suaranya berakhir bersama aliran udara.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-jim-syin-ya','makhraj','Tengah lidah: jim, syin dan ya',ARRAY['ج','ش','ي','jim','syin','ya bukan mad']::text[],'المقدمة الجزرية','الإمام ابن الجزري','13 (petikan)','وَالْوَسْطُ: فَجِيمُ الشِّينُ يَا','Jim, syin dan ya bukan mad keluar daripada bahagian tengah lidah.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-khaisyum','makhraj','Al-Khaisyum (rongga hidung)',ARRAY['khaisyum','ghunnah','dengung','hidung','الخيشوم']::text[],'المقدمة الجزرية','الإمام ابن الجزري','19 (bahagian kedua)','وَغُنَّةٌ: مَخْرَجُهَا الْخَيْشُومُ','Dengung (ghunnah) keluar melalui rongga hidung (al-khaisyum).','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-nun-ra','makhraj','Makhraj nun dan ra',ARRAY['ن','ر','nun','ra','hujung lidah']::text[],'المقدمة الجزرية','الإمام ابن الجزري','15','وَالنُّونُ: مِنْ طَرَفِهِ تَحْتُ اجْعَلُوا
وَالرَّا: يُدَانِيهِ لِظَهْرٍ أَدْخَلُ','Nun keluar daripada hujung lidah di bawah makhraj lam; ra berdekatan dengannya, sedikit ke arah belakang lidah.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-qaf-kaf','makhraj','Makhraj qaf dan kaf',ARRAY['ق','ك','qaf','kaf','pangkal lidah']::text[],'المقدمة الجزرية','الإمام ابن الجزري','12–13 (petikan)','وَالْقَافُ أَقْصَى اللِّسَانِ فَوْقُ، ثُمَّ الْكَافُ أَسْفَلُ','Qaf keluar daripada bahagian paling belakang lidah yang lebih atas; kaf pula pada kawasan belakang lidah yang sedikit lebih rendah.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('makhraj-syafatain','makhraj','Dua bibir',ARRAY['syafatain','الشفتين','و','ب','م','wau','ba','mim']::text[],'المقدمة الجزرية','الإمام ابن الجزري','19 (bahagian pertama)','لِلشَّفَتَيْنِ: الْوَاوُ بَاءٌ مِيمُ','Wau bukan mad, ba dan mim keluar melalui dua bibir.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('sifat-berlawanan','sifat','Sifat yang berlawanan',ARRAY['sifat berlawanan','hams jahar','رِخو','jahar','رخاوة']::text[],'المقدمة الجزرية','الإمام ابن الجزري','20','صِفَاتُهَا: جَهْرٌ، وَرِخْوٌ، مُسْتَفِلْ
مُنْفَتِحٌ، مُصْمَتَةٌ، وَالضِّدَّ: قُلْ','Antara sifat huruf ialah jahr, rikhawah, istifal, infitah dan ismat; sebutkan juga sifat-sifat lawannya.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('sifat-hams-syiddah','sifat','Hams dan syiddah',ARRAY['hams','همس','hamsah','فحثه شخص سكت','syiddah','شدة','أجد قط بكت']::text[],'المقدمة الجزرية','الإمام ابن الجزري','21','مَهْمُوسُهَا: «فَحَثَّهُ شَخْصٌ سَكَتْ»
شَدِيدُهَا: لَفْظُ «أَجِدْ قَطٍ بَكَتْ»','Huruf hams terkumpul dalam ungkapan ''فحثه شخص سكت''; huruf syiddah terkumpul dalam ''أجد قط بكت''.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('sifat-inhiraf-takrir','sifat','Inhiraf, takrir, tafasyi dan istitalah',ARRAY['inhiraf','انحراف','takrir','تكرير','tafasyi','تفشي','istitalah','استطالة']::text[],'المقدمة الجزرية','الإمام ابن الجزري','26','فِي اللَّامِ وَالرَّا، وَبِتَكْرِيرٍ جُعِلْ
وَلِلتَّفَشِّي: الشِّينُ، ضَاداً: اسْتَطِلْ','Inhiraf berlaku pada lam dan ra; ra juga mempunyai takrir. Syin mempunyai tafasyi dan dhad mempunyai istitalah.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('sifat-itbaq-izlaq','sifat','Itbaq dan izlaq',ARRAY['itbaq','إطباق','izlaq','إذلاق','ص ض ط ظ','فر من لب']::text[],'المقدمة الجزرية','الإمام ابن الجزري','23','وَصَادُ ضَادٌ طَاءُ ظَاءٌ: مُطْبَقَهْ
وَ«فَرَّ مِنْ لُبِّ»: الْحُرُوفُ الْمُذْلَقَهْ','Huruf itbaq ialah ص، ض، ط، ظ. Huruf izlaq terkumpul dalam ungkapan ''فر من لب''.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('sifat-lin','sifat','Sifat lin',ARRAY['lin','لين','wau lin','ya lin','huruf lembut']::text[],'المقدمة الجزرية','الإمام ابن الجزري','25','وَاوٌ وَيَاءٌ سُكِّنَا وَانْفَتَحَا
قَبْلَهُمَا، وَالِانْحِرَافُ صُحِّحَا','Huruf lin ialah wau dan ya yang sukun serta didahului fathah; bait ini juga menghubungkan perbahasan kepada sifat inhiraf.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('sifat-safir-qalqalah','sifat','Safir dan qalqalah',ARRAY['safir','صفير','qalqalah','قلقلة','قطب جد','lantunan']::text[],'المقدمة الجزرية','الإمام ابن الجزري','24','صَفِيرُهَا: صَادٌ وَزَايٌ سِينُ
قَلْقَلَةٌ: «قُطْبُ جَدٍ»، وَاللِّينُ','Huruf safir ialah ص، ز، س; huruf qalqalah ialah ق، ط، ب، ج، د. Bait ini kemudian menyambung perbincangan sifat lin.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('sifat-tawassut-istila','sifat','Tawassut dan isti‘la’',ARRAY['tawassut','wasat','لن عمر','isti''la','استعلاء','خص ضغط قظ','tebal']::text[],'المقدمة الجزرية','الإمام ابن الجزري','22','وَبَيْنَ رِخْوٍ وَالشَّدِيدِ: «لِنْ عُمَرْ»
وَسَبْعُ عُلْوٍ: «خُصَّ ضَغْطٍ قِظْ» حَصَرْ','Huruf tawassut (pertengahan antara rikhawah dengan syiddah) ialah ''لن عمر''; tujuh huruf isti‘la’ terkumpul dalam ''خص ضغط قظ''.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-dhad-zha','tajwid','Membezakan dhad dan zha',ARRAY['ض','ظ','dhad dan zha','dad za','istitalah']::text[],'المقدمة الجزرية','الإمام ابن الجزري','52 (petikan)','وَالضَّادَ بِاسْتِطَالَةٍ وَمَخْرَجِ
مَيِّزْ مِنَ الظَّاءِ','Bezakan dhad (ض) daripada zha (ظ) melalui sifat istitalah dan makhrajnya.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-ghunnah-tuhfah','tajwid','Ghunnah mim dan nun musyaddadah',ARRAY['dengung mim nun','mim nun sabdu','غنة']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','17','وَغُنَّ مِيمًا ثُمَّ نُونًا شُدِّدَا
وَسَمِّ كُلًّا حَرْفَ غُنَّةٍ بَدَا','Dengungkan mim dan nun yang bersabdu; kedua-duanya dinamakan huruf ghunnah.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-hak-huruf','tajwid','Definisi tajwid: hak dan mustahak huruf',ARRAY['takrif tajwid','definisi tajwid','hak huruf','mustahak huruf','حقها','التجويد']::text[],'المقدمة الجزرية','الإمام ابن الجزري','30','وَهُوَ: «إِعْطَاءُ الْحُرُوفِ حَقَّهَا
مِنْ صِفَةٍ لَهَا وَمُسْتَحَقَّهَا»','Tajwid ialah memberikan setiap huruf haknya berupa sifat-sifat yang tetap, serta sifat yang menjadi tuntutannya ketika bacaan.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-idgham','tajwid','Idgham nun sukun dan tanwin',ARRAY['idgham','idgham bighunnah','يرملون','ينمو']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','9–10','وَالثَّانِي إِدْغَامٌ بِسِتَّةٍ أَتَتْ
فِي يَرْمَلُونَ عِنْدَهُمْ قَدْ ثَبَتَتْ
لَكِنَّهَا قِسْمَانِ قِسْمٌ يُدْغَمَا
فِيهِ بِغُنَّةٍ بِيَنْمُو عُلِمَا','Idgham mempunyai enam huruf terkumpul dalam ''يرملون''; empat daripadanya (ي، ن، م، و) termasuk idgham dengan dengung.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-idgham-bila','tajwid','Idgham bila ghunnah',ARRAY['idgham bila ghunnah','idgham tanpa dengung','lam ra','ل ر']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','12','وَالثَّانِي إِدْغَامٌ بِغَيْرِ غُنَّهْ
فِي اللَّامِ وَالرَّا ثُمَّ كَرِّرَنَّهْ','Idgham tanpa dengung berlaku apabila nun sukun atau tanwin bertemu lam atau ra.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-idgham-mithlain','tajwid','Idgham mithlain syafawi',ARRAY['idgham mimi','idgham mithlain','mim mati mim','م م']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','21','وَالثَّانِي إِدْغَامٌ بِمِثْلِهَا أَتَى
وَسَمِّ إِدْغَامًا صَغِيرًا يَا فَتَى','Idgham mim sukun berlaku apabila bertemu mim seumpamanya, dan dinamakan idgham kecil (saghir).','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-ikhfa-haqiqi','tajwid','Ikhfa haqiqi dan 15 hurufnya',ARRAY['ikhfa','ikhfa haqiqi','اخفاء','15 huruf ikhfa','صف ذا ثنا']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','14–16','وَالرَّابِعُ الْإِخْفَاءُ عِنْدَ الْفَاضِلِ
مِنَ الْحُرُوفِ وَاجِبٌ لِلْفَاضِلِ
فِي خَمْسَةٍ مِنْ بَعْدِ عَشْرٍ رَمْزُهَا
فِي كِلْمِ هَذَا الْبَيْتِ قَدْ ضَمَّنْتُهَا
صِفْ ذَا ثَنَا كَمْ جَادَ شَخْصٌ قَدْ سَمَا
دُمْ طَيِّبًا زِدْ فِي تُقًى ضَعْ ظَالِمَا','Ikhfa berlaku dengan lima belas huruf yang diwakili huruf pertama setiap perkataan pada bait terakhir.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-ikhfa-syafawi','tajwid','Ikhfa syafawi',ARRAY['ikhfa syafawi','mim mati bertemu ba','اخفاء شفوي','م ب']::text[],'المقدمة الجزرية','الإمام ابن الجزري','63','الْمِيمَ إِنْ تَسْكُنْ بِغُنَّةٍ لَدَى
بَاءٍ عَلَى الْمُخْتَارِ مِنْ أَهْلِ الْأَدَا','Mim sukun di hadapan ba dibaca secara ikhfa dengan ghunnah menurut pendapat pilihan ahli qiraat.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-iqlab','tajwid','Iqlab',ARRAY['iqlab','ikhfa iqlab','nun mati ba','إقلاب','ن ب']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','13','وَالثَّالِثُ الْإِقْلَابُ عِنْدَ الْبَاءِ
مِيمًا بِغُنَّةٍ مَعَ الْإِخْفَاءِ','Iqlab berlaku apabila nun sukun atau tanwin bertemu ba: bunyinya ditukar kepada mim secara samar dengan dengung.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-izhar-halqi','tajwid','Izhar halqi',ARRAY['izhar halqi','izhar halki','اظهار حلقي','ء ه ع ح غ خ']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','7–8','فَالْأَوَّلُ الْإِظْهَارُ قَبْلَ أَحْرُفِ
لِلْحَلْقِ سِتٌّ رُتِّبَتْ فَلْتَعْرِفِ
هَمْزٌ فَهَاءٌ ثُمَّ عَيْنٌ حَاءُ
مُهْمَلَتَانِ ثُمَّ غَيْنٌ خَاءُ','Hukum pertama ialah izhar apabila nun sukun atau tanwin bertemu enam huruf halqi: ء، ه، ع، ح، غ، خ.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-izhar-mutlaq','tajwid','Izhar mutlaq dalam satu kalimah',ARRAY['izhar mutlaq','dunia','صنوان','دنيا','satu kalimah']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','11','إِلَّا إِذَا كَانَا بِكِلْمَةٍ فَلَا
تُدْغِمْ كَدُنْيَا ثُمَّ صِنْوَانٍ تَلَا','Apabila nun sukun dan huruf idgham tertentu berada dalam satu perkataan, nun tidak diidghamkan, seperti ''دنيا'' dan ''صنوان''.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-izhar-syafawi','tajwid','Izhar syafawi',ARRAY['izhar syafawi','mim mati','اظهار شفوي','م ف','م و']::text[],'المقدمة الجزرية','الإمام ابن الجزري','64','وَأَظْهِرَنْهَا عِنْدَ: بَاقِي الْأَحْرُفِ
وَاحْذَرْ لَدَى وَاوٍ وَفَا: أَنْ تَخْتَفِي','Zahirkan mim sukun di hadapan huruf lain, dan berhati-hati agar tidak menyembunyikannya ketika bertemu wau atau fa.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-lam-allah','tajwid','Tebal lam pada lafaz Allah',ARRAY['lam jalalah','lafzul jalalah','الله','تفخيم اللام']::text[],'المقدمة الجزرية','الإمام ابن الجزري','44','وَفَخِّمِ اللَّامَ مِنِ اسْمِ «اللَّهِ»
عَنْ فَتْحٍ أَوْ ضَمٍّ كَـ «عَبْدُ اللَّهِ»','Tebalkan lam pada lafaz Allah apabila didahului fathah atau dammah.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-lam-qamari','tajwid','Lam qamariyyah',ARRAY['lam qamariyyah','al qamariah','ال القمرية','ابغ حجك وخف عقيمه']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','24–25','لِلَامِ أَلْ حَالَانِ قَبْلَ الْأَحْرُفِ
أُولَاهُمَا إِظْهَارُهَا فَلْتَعْرِفِ
قَبْلَ أَرْبَعٍ مَعْ عَشْرَةٍ خُذْ عِلْمَهُ
مِنِ ابْغِ حَجَّكَ وَخَفْ عَقِيمَهُ','Lam pada alif-lam dibaca jelas di hadapan empat belas huruf qamariyyah yang dirangkum dalam ''ابغ حجك وخف عقيمه''.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-lam-syamsi','tajwid','Lam syamsiyyah',ARRAY['lam syamsiyyah','al syamsiah','الشمسية','طب ثم صل','lam matahari']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','26–28','ثَانِيهِمَا إِدْغَامُهَا فِي أَرْبَعٍ
وَعَشْرَةٍ أَيْضًا وَرَمْزَهَا فَعِ
طِبْ ثُمَّ صِلْ رُحْمًا تَفُزْ ضِفْ ذَا نِعَمْ
دَعْ سُوءَ ظَنٍّ زُرْ شَرِيفًا لِلْكَرَمْ','Lam syamsiyyah diidghamkan apabila bertemu salah satu daripada empat belas hurufnya; huruf awal setiap kata dalam bait ini ialah petunjuknya.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-arid','tajwid','Mad ‘arid lissukun',ARRAY['arid lissukun','mad arid','عارض للسكون','waqaf mad']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','45','وَمِثْلُ ذَا إِنْ عَرَضَ السُّكُونُ
وَقْفًا كَتَعْلَمُونَ نَسْتَعِينُ','Mad ‘arid lissukun berlaku kerana sukun yang timbul ketika waqaf; contohnya ''تعلمون'' dan ''نستعين''.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-badal','tajwid','Mad badal',ARRAY['mad badal','بدل','آمنوا']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','46','أَوْ قُدِّمَ الْهَمْزُ عَلَى الْمَدِّ وَذَا
بَدَلْ كَآمَنُوا وَإِيمَانًا خُذَا','Mad badal berlaku apabila hamzah mendahului huruf mad seperti dalam ''آمنوا'' dan ''إيمانًا''.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-fari','tajwid','Mad far‘i',ARRAY['mad fari','mad far''i','المد الفرعي','hamzah sukun']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','38','وَالْآخَرُ الْفَرْعِيُّ مَوْقُوفٌ عَلَى
سَبَبٍ كَهَمْزٍ أَوْ سُكُونٍ مُسْجَلَا','Mad far‘i bergantung pada sebab seperti hamzah atau sukun.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-lazim','tajwid','Mad lazim',ARRAY['mad lazim','مد لازم','sukun asli']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','47','وَلَازِمٌ إِنِ السُّكُونُ أُصِّلَا
وَصْلًا وَوَقْفًا بَعْدَ مَدٍّ طُوِّلَا','Mad lazim berlaku apabila huruf mad diikuti sukun asli yang kekal ketika wasal dan waqaf.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-lazim-empat','tajwid','Empat jenis mad lazim',ARRAY['mad lazim kalimi','mad lazim harfi','muthaqqal','mukhaffaf','أقسام لازم']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','48–49','أَقْسَامُ لَازِمٍ لَدَيْهِمْ أَرْبَعَةْ
وَتِلْكَ كِلْمِيٌّ وَحَرْفِيٌّ مَعَهْ
كِلَاهُمَا مُخَفَّفٌ مُثَقَّلُ
فَهَذِهِ أَرْبَعَةٌ تُفَصَّلُ','Mad lazim ada empat bahagian: kalimi muthaqqal, kalimi mukhaffaf, harfi muthaqqal dan harfi mukhaffaf.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-munfasil','tajwid','Mad jaiz munfasil',ARRAY['jaiz munfasil','mad munfasil','جائز منفصل','hamzah dua perkataan']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','44','وَجَائِزٌ مَدٌّ وَقَصْرٌ إِنْ فُصِلْ
كُلٌّ بِكِلْمَةٍ وَهَذَا الْمُنْفَصِلْ','Mad jaiz munfasil berlaku apabila huruf mad berada pada akhir suatu perkataan dan hamzah pada awal perkataan berikutnya.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-muttasil','tajwid','Mad wajib muttasil',ARRAY['wajib muttasil','mad muttasil','واجب متصل','hamzah satu perkataan']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','43','فَوَاجِبٌ إِنْ جَاءَ هَمْزٌ بَعْدَ مَدْ
فِي كِلْمَةٍ وَذَا بِمُتَّصِلٍ يُعَدْ','Mad wajib muttasil berlaku apabila hamzah datang selepas huruf mad dalam perkataan yang sama.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mad-tabi','tajwid','Mad asli (tabi‘i)',ARRAY['mad asli','mad tabii','mad tabi''i','المد الطبيعي','2 harakat']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','35–37','وَالْمَدُّ أَصْلِيٌّ وَفَرْعِيٌّ لَهُ
وَسَمِّ أَوَّلًا طَبِيعِيًّا وَهُوَ
مَا لَا تَوَقُّفٌ لَهُ عَلَى سَبَبْ
وَلَا بِدُونِهِ الْحُرُوفُ تُجْتَلَبْ','Mad dibahagi kepada asli dan far‘i. Mad asli atau tabi‘i tidak bergantung pada sebab hamzah atau sukun.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-melatih-bacaan','tajwid','Tajwid tanpa berlebih-lebihan',ARRAY['latihan','takalluf','تعسف','tanpa memaksa']::text[],'المقدمة الجزرية','الإمام ابن الجزري','31–33','وَرَدُّ كُلِّ وَاحِدٍ لِأَصْلِهِ
وَاللَّفْظُ فِي نَظِيرِهِ كَمِثْلِهِ
مُكَمَّلًا مِنْ غَيْرِ مَا تَكَلُّفِ
بِاللُّطْفِ فِي النُّطْقِ بِلَا تَعَسُّفِ','Kembalikan setiap huruf kepada asalnya, samakan sebutan huruf yang sejenis, dan sempurnakan bacaan secara lembut tanpa dibuat-buat.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-mim-tiga','tajwid','Tiga hukum mim sakinah',ARRAY['hukum mim mati','mim sakinah','أحكام الميم']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','19','أَحْكَامُهَا ثَلَاثَةٌ لِمَنْ ضَبَطْ
إِخْفَاءٌ ادْغَامٌ وَإِظْهَارٌ فَقَطْ','Mim sukun mempunyai tiga hukum: ikhfa, idgham dan izhar.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mutajanisain','tajwid','Mutajanisain',ARRAY['mutajanisain','متجانسين','sama makhraj']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','32–33 (petikan)','أَوْ يَكُونَا اتَّفَقَا
فِي مَخْرَجٍ دُونَ الصِّفَاتِ حُقِّقَا
بِالْمُتَجَانِسَيْنِ','Dua huruf yang sama makhraj tetapi berbeza sifatnya dinamakan mutajanisain.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mutamathilain','tajwid','Mutamathilain',ARRAY['mutamathilain','متماثلين','dua huruf sama']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','30','إِنْ فِي الصِّفَاتِ وَالْمَخَارِجِ اتَّفَقْ
حَرْفَانِ فَالْمِثْلَانِ فِيهِمَا أَحَقْ','Dua huruf yang sama makhraj dan sifatnya dinamakan mutamathilain.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-mutaqaribain','tajwid','Mutaqaribain',ARRAY['mutaqaribain','متقاربين','makhraj hampir']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','31–32 (petikan)','وَإِنْ يَكُونَا مَخْرَجًا تَقَارَبَا
وَفِي الصِّفَاتِ اخْتَلَفَا يُلَقَّبَا
مُتَقَارِبَيْنِ','Dua huruf yang berdekatan makhrajnya dan berbeza sifatnya dinamakan mutaqaribain menurut pengelasan yang dijelaskan dalam matan ini.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-nun-empat','tajwid','Empat hukum nun sakinah dan tanwin',ARRAY['nun sakinah','nun mati','tanwin','empat hukum nun','تنوين']::text[],'تحفة الأطفال','الإمام سليمان الجمزوري','6','لِلنُّونِ إِنْ تَسْكُنْ وَلِلتَّنْوِينِ
أَرْبَعُ أَحْكَامٍ فَخُذْ تَبْيِينِي','Nun sukun dan tanwin mempunyai empat hukum bacaan: izhar, idgham, iqlab dan ikhfa.','https://ar.wikisource.org/wiki/تحفة_الأطفال','reviewed'),
('tajwid-nun-mim-musya','tajwid','Ghunnah pada nun dan mim bersabdu',ARRAY['ghunnah musyaddadah','nun sabdu','mim sabdu','نّ','مّ']::text[],'المقدمة الجزرية','الإمام ابن الجزري','62 (petikan)','وَأَظْهِرِ الْغُنَّةَ مِنْ نُونٍ، وَمِنْ
مِيمٍ؛ إِذَا مَا شُدِّدَا','Nyatakan dengung pada nun dan mim apabila kedua-duanya bersabdu.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-ra-tarqiq','tajwid','Ra nipis (tarqiq)',ARRAY['ra nipis','tarqiq ra','ترقيق الراء','ر','ra kasrah']::text[],'المقدمة الجزرية','الإمام ابن الجزري','41–42','وَرَقِّقِ الرَّاءَ إِذَا مَا كُسِرَتْ
كَذَاكَ بَعْدَ الْكَسْرِ حَيْثُ سَكَنَتْ
إِنْ لَمْ تَكُنْ مِنْ قَبْلِ حَرْفِ اسْتِعْلَا
أَوْ كَانَتِ الْكَسْرَةُ لَيْسَتْ أَصْلَا','Nipiskan ra apabila berbaris kasrah; begitu juga ra sukun selepas kasrah dengan syarat-syarat yang disebut dalam sambungan bait.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-tafkhim','tajwid','Tafkhim huruf isti‘la’',ARRAY['tafkhim','tebal','huruf isti''la','استعلاء']::text[],'المقدمة الجزرية','الإمام ابن الجزري','45','وَحَرْفَ الِاسْتِعْلَاءِ فَخِّمْ، وَاخْصُصَا
لِإِطْبَاقَ أَقْوَى؛ نَحْوُ: «قَالَ» وَ«الْعَصَا»','Tebalkan huruf isti‘la’; huruf itbaq mempunyai kekuatan penebalan yang lebih khusus.','https://surahquran.com/Tajweed/aljazariah.html','reviewed'),
('tajwid-waqaf','tajwid','Waqaf dan ibtida’',ARRAY['waqaf','wakaf','ibtida','وقف','tam','kafi','hasan']::text[],'المقدمة الجزرية','الإمام ابن الجزري','73–74','وَبَعْدَ تَجْوِيدِكَ لِلْحُرُوفِ
لَا بُدَّ مِنْ مَعْرِفَةِ الْوُقُوفِ
وَالِابْتِدَاءِ، وَهْيَ تُقْسَمُ إِذَنْ
ثَلَاثَةً: تَامٌّ، وَكَافٍ، وَحَسَنْ','Selepas memperelok sebutan huruf, seseorang perlu mengetahui ilmu waqaf dan ibtida’. Pembahagian yang disebut ialah tam, kafi dan hasan.','https://surahquran.com/Tajweed/aljazariah.html','reviewed')
ON CONFLICT (slug) DO UPDATE SET category=excluded.category,topic=excluded.topic,aliases=excluded.aliases,source_title=excluded.source_title,source_author=excluded.source_author,source_verse=excluded.source_verse,arabic_text=excluded.arabic_text,meaning_ms=excluded.meaning_ms,source_url=excluded.source_url,verification_status=excluded.verification_status;
COMMIT;
