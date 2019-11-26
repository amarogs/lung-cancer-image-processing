import tciaclient
import pandas

def getResponseString(response):
    if response.getcode() is not 200:
        raise ValueError("Server returned an error")
    else:
        return response.read()


api_key = "16ade9bc-f2fa-4a37-b357-36466a0020fc"
baseUrl = "https://services.cancerimagingarchive.net/services/v3"
resource = "TCIA"

client = tciaclient.TCIAClient(api_key, baseUrl, resource)

response = client.get_modality_values()
strRespModalities = getResponseString(response)
#CT modality is 1
#print(pandas.io.json.read_json(strRespModalities))
#CHEST is body_part 0

response = client.get_series(modality="CT", collection="LungCT-Diagnosis")
strRespSeries = getResponseString(response)

pdfSeries = pandas.io.json.read_json(strRespSeries)

strSeriesUID = pdfSeries.ix[2].SeriesInstanceUID
response = client.get_image(strSeriesUID)
strResponseImage = getResponseString(response)

with open("images.zip", "wb") as fid:
    fid.write(strResponseImage)
    fid.close()
