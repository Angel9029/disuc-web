#!/usr/bin/env python3
"""
Script de prueba para validar la carga de CSV
Uso: python test_upload.py
"""

import requests
import os
import time

BASE_URL = "http://localhost:8000"
DATA_DIR = "data"

def test_health():
    """Verifica que el servidor esté activo"""
    print("\n🔍 Verificando servidor...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor activo")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def upload_file(file_type, file_path):
    """Carga un archivo CSV"""
    if not os.path.exists(file_path):
        print(f"  ⚠️  {file_type}: Archivo no encontrado ({file_path})")
        return False
    
    print(f"  📤 {file_type.upper()}...", end=" ", flush=True)
    
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{BASE_URL}/api/upload/{file_type}",
                files={"file": f}
            )
        
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"❌ {data['error']}")
                return False
            elif "errores" in data:
                print(f"⚠️  {data['cargados']} registros, {len(data['errores'])} errores")
                for err in data['errores'][:2]:
                    print(f"     - {err}")
                return True
            else:
                msg = data.get("mensaje", "Cargado")
                print(f"✅ {msg}")
                return True
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {str(e)}")
        return False

def get_status():
    """Obtiene el estado de la base de datos"""
    print("\n📊 Estado de la base de datos:")
    try:
        response = requests.get(f"{BASE_URL}/api/upload/status")
        if response.status_code == 200:
            data = response.json()
            print(f"  • Clientes: {data.get('clientes', 0)}")
            print(f"  • Productos: {data.get('productos', 0)}")
            print(f"  • Ventas: {data.get('ventas', 0)}")
            print(f"  • Pedidos: {data.get('pedidos', 0)}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🧪 DISUC - Script de Prueba de Carga de CSV")
    print("=" * 60)
    
    # 1. Verificar servidor
    if not test_health():
        print("\n⚠️  El servidor no está activo.")
        print("Ejecuta: uvicorn app.main:app --reload")
        return
    
    # 2. Estado inicial
    print("\n📥 Estado inicial:")
    get_status()
    
    # 3. Cargar archivos de ejemplo
    print("\n📤 Cargando archivos de ejemplo...")
    
    files_to_load = [
        ("clientes", f"{DATA_DIR}/ejemplo_clientes.csv"),
        ("categorias", f"{DATA_DIR}/ejemplo_categorias.csv"),
        ("productos", f"{DATA_DIR}/ejemplo_productos.csv"),
        ("ventas", f"{DATA_DIR}/ejemplo_ventas.csv"),
    ]
    
    loaded = 0
    for file_type, file_path in files_to_load:
        if upload_file(file_type, file_path):
            loaded += 1
        time.sleep(0.5)  # Pequeña pausa entre uploads
    
    # 4. Estado final
    print("\n✨ Estado final:")
    get_status()
    
    # 5. Resumen
    print("\n" + "=" * 60)
    if loaded > 0:
        print(f"✅ Se cargaron {loaded}/{len(files_to_load)} archivos exitosamente")
    else:
        print("⚠️  No se cargaron archivos. Verifica que existan en /data/")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba cancelada")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
