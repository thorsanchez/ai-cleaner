# Sjálfvirkt kerfi sem notar gervigreind til að greina og forgangsraða viðskiptaatvik

## Um Verkefnið

- Sækir gögn frá mörgum stöðum (API, CSV skrár)
- Hreinsar gögnin
- Notar gervigreind (Gemini) til að flokka alvarleika tickets
- sendir viðvaranir sjálfkrafa fyrir alvarleg mál
- Keyrir í skýinu á AWS með Docker og Terraform
- Kerfið notar llm sem ákvörðunarvél, ekki bara textaframleiðslu

## Markmið

Fyrirtæki fá þúsundir tickets, villa og endurgjafir á hverjum degi. Þetta kerfi:
- forgangsraðar sjálfkrafa mikilvægum málum
- Minnkar viðbragðstíma
- gefur skipulagðar ákvarðanir (alvarleiki, flokkur, ráðlögð aðgerð)

## Project Structure
![projectstructure](image.png)

## Uppbygging

Gögn (git api, csv) -> Python gagnavinnsla -> llm -> Sjálfvirkar alerts

## Tækni

- Pthon
- Docker
- Terraform
- AWS EC2


### Skilar
```json
{
  "severity": "critical",
  "category": "performance",
  "recommended_action": "escalate",
  "confidence": 0.95,
  "reasoning": "Þjónustutruflanir sem hafa áhrif á alla notendur"
}
```

### Alvarleikastig dæmi:
- **Critical** - Kerfi niðri 
- **High** - Stór villa, margir notendur, tekjuáhrif
- **Medium** - Minniháttar villa
- **Low** - Útlitsvilla, stakur notandi


## AWS 

Terraform býr til:
- EC2 Instance
- SSH
- IAM Role
- Docker