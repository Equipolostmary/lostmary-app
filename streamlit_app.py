from drive_upload import conectar_drive, subir_archivo_a_drive

# ...

if st.button("Subir promociones"):
    if not imagenes:
        st.warning("Debes seleccionar al menos una imagen.")
    else:
        # Conectar a Google Drive
        service = conectar_drive("service_account.json")
        
        # Carpeta de destino desde el Excel
        carpeta_id = punto["Carpeta Drive"]
        
        # Subir una por una
        for imagen in imagenes:
            nombre_archivo = imagen.name
            subir_archivo_a_drive(service, imagen, nombre_archivo, carpeta_id)

        # Mostrar confirmación
        st.success(f"✅ Se subieron {len(imagenes)} imagen(es) a tu carpeta de Drive.")
        st.write("📁 Carpeta:", punto["Carpeta Drive"])
