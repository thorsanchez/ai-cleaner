# Automation Verkefnasafn

Þetta repo inniheldur ýmis AI og data analysis automation verkefni sem sýna færni í Python, AI integration, cloud deployment og gagnagreiningu.

## Verkefni

### `cloud-ai-workflows/`

Sjálfvirkt incident management kerfi sem sækir tickets úr mörgum áttum, notar AI til að flokka alvarleika atvika og sendir viðvaranir fyrir mikilvæg mál (deployed á AWS með Docker og Terraform).
![output](./cloud-ai-workflows/public/output.png)

### `ai_data_processing_pipeline/`

Data processing pipeline sem les athugasemdir viðskiptavina úr CSV, hreinsar texta og notar Google Gemini AI fyrir sentiment analysis og samantekt á íslensku.
![table](./public/Screenshot%202026-01-05%20at%2016.23.03.png)

### `ai_feedback/`

Sækir athugasemdir viðskiptavina úr API, hreinsar textann og notar Google Gemini AI til að búa til markdown skýrslur sem greina sentiment og lykilatriði.
![output](./ai_feedback/Screenshot%202026-01-05%20at%2016.36.29.png)

### `ai_insight-dashboard/`

Streamlit dashboard sem safnar saman feedback frá mörgum stöðum og notar Google Gemini AI til að búa til insights með sentiment analysis og ráðleggingum.
![output](./ai_insight-dashboard/image.png)

### `automation-statistics/`

Dynamic univariate analysis sem er automated og virkar fyrir hvaða pandas DataFrame sem er
![output](./automation-statistics/Screenshot5.1.png)
![output](./automation-statistics/Screenshot5.2-2.png)
