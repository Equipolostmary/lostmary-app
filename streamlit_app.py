[gcp_service_account]
type = "service_account"
project_id = "tu-proyecto-id"
private_key_id = "tu-private-key-id"
private_key = """
-----BEGIN PRIVATE KEY-----
...tu clave privada aquí...
-----END PRIVATE KEY-----
"""
client_email = "tu-email@tu-proyecto.iam.gserviceaccount.com"
client_id = "tu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "url-certificado-x509"
sheet_id = "ID_de_tu_hoja_de_calculo_google_sheets"
