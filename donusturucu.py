# MP4 TO MP3 CONVERSION SCRIPT
# Bu script mp4 dosyalarini mp3 dosyalarina ceviriyor. 
# Kullanimi: python mp4tomp3.py
# sudo apt-get install lame
# sudo apt-get install mplayer
# sudo apt-get install python2.7


from subprocess import call
import os

def DosyaKontrol(dizin, dosya_ismi, uzanti):
    yol = dizin + "/" + dosya_ismi + uzanti
    return os.path.isfile(yol)

def main(girisDizini, cikisDizini):


    try:
        # Belirtilen dizinler kontrol ediliyor.
        if not os.path.exists(girisDizini):
            exit("Hata: Giris dizini \'" + girisDizini + "\' bulunamiyor.")
        if not os.path.exists(cikisDizini):
            exit("Hata: Cikis dizini \'" + cikisDizini + "\' bulunamiyor.")
        if not os.access(cikisDizini, os.W_OK):
            exit("Hata: Cikis dizinine \'" + cikisDizini + "\' yazilamiyor.")

        print "[%s/*.mp4] --> [%s/*.mp3]" % (girisDizini, cikisDizini)
        dosyalar = [] # Dosya listesi
            
        # Donusum yapilacak olan dizindeki mp4 formatindaki dosyalari buluyor.
        dosyaListesi = [ f for f in os.listdir(girisDizini) if f.endswith(".mp4") ]
        for yol in dosyaListesi:
            d_isim = os.path.basename(yol) 
            dosya_ismi = os.path.splitext(d_isim)[0]
            dosyalar.append(dosya_ismi)

        dosyalar[:] = [f for f in dosyalar if not DosyaKontrol(cikisDizini, f, ".mp3")]
    except OSError as e:
        exit(e)
    
    if len(dosyalar) == 0:
        exit("Donusturme yapmak icin dosya bulunamadi.")

    # convert all unconverted files
    for dosya_ismi in dosyalar:
        print "-- Donusum %s.mp4 --> %s.mp3 --" % (girisDizini + "/" + dosya_ismi, cikisDizini + "/" + dosya_ismi)
        call(["mplayer", "-novideo", "-nocorrect-pts", "-ao", "pcm:waveheader", girisDizini + "/" + dosya_ismi + ".mp4"])
        call(["lame", "-h", "-b", "192", "audiodump.wav", cikisDizini + "/" + dosya_ismi + ".mp3"])
        os.remove("audiodump.wav")

# dizin bilgilerini giriniz.
args = {"girisDizini":"yol","cikisDizini":"yol"}
main(args["girisDizini"], args["cikisDizini"])
