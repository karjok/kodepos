from requests import get,post
import re,json

def get_prov():
	r = get("https://m.nomor.net/_kodepos.php?_i=provinsi-kodepos").text
	provs = re.findall(r"td\ align\=\"left\".*?href\=\"(.*?)\".*?\>(.*?)\<",r)
	return provs
def get_kab(prov):
	r = get(prov).text
	kabs = re.findall(r"td\ align\=\"left\".*?href\=\"(.*?)\".*?\>(.*?)\<",r)
	return kabs
def get_kec(kab):
	r = get(kab).text
	kecs = re.findall(r"td\ align\=\"center\"\>\d+\<.*?\<a\ href\=\"(.*?)\".*?\>([a-zA-Z\ \'\"\/\(\)\-]+)\<\/a.*?\<td\ align\=\"center\".*?\<a\ href\=.*?\>(\d+)\<\/a",r)
	return kecs
def get_kel(kec):
	r = get(kec).text
	kels = re.findall(r"td\ align\=\"center\"\>\d+\<\/td\>.*?\<a\ href\=.*?\"\>(\d+)\<\/a.*?td\>\<a.*?\>([a-zA-Z\ \'\"\/\(\)\-]+)\<\/a",r)
	return kels
def main():
	data = []
	prov_n = 1
	for prov in get_prov():
	    print("*",prov_n,prov[1])
	    kab_n = 1
	    kabs = []
	    ka = get_kab(prov[0])
	    print("\033[93m  *terdapat",len(ka),"kabupaten\033[0m")
	    for kab in ka[:1]:
	        print("   *",kab_n,kab[1])
	        kecs = []
	        kec_n = 1
	        ke = get_kec(kab[0])
	        for kec in ke:
	            kels = []
	            kel_n = 1
	            for kel in get_kel(kec[0]):
	                kel = {"kelurahan":kel[1],"kode pos":kel[0]}
	                kels.append(kel)
	                kel_n += 1
	            kecs.append({"kecamatan":kec[1],"jumlah_kelurahan":len(kels),"daftar_kelurahan":kels})
	            print(f"    > {round((len(kecs)/len(ke))*100)}%\r",end="")
	            kec_n +=1
	        kabs.append({"kabupaten":kab[1],"jumlah_kecamatan":len(kecs),"daftar_kecamatan":kecs})
	        kab_n += 1
	    data.append({"provinsi":prov[1],"jumlah_kabupaten":len(kabs),"daftar_kabupaten":kabs})
	    prov_n += 1
	    break
	json.dump({"data":data},open("kodepos.json","w"),indent=2)
