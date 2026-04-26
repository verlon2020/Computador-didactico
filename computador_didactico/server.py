#!/usr/bin/env python3
"""
🖥️ ¡Arma tu Computador! - Servidor Local
Para niños de 8 años - Aprende las piezas del PC jugando
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class ColorPrint:
    """Imprime mensajes con colores en la terminal"""
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def banner():
        print(f"""
{ColorPrint.PURPLE}{ColorPrint.BOLD}
╔══════════════════════════════════════════════════════╗
║   🖥️  ¡ARMA TU COMPUTADOR!  🔧                       ║
║   Aprende las piezas del PC jugando                  ║
║   Hecho para niños de 8 años 🌟                      ║
╚══════════════════════════════════════════════════════╝
{ColorPrint.END}""")

    @staticmethod
    def ok(msg):
        print(f"  {ColorPrint.GREEN}✅ {msg}{ColorPrint.END}")

    @staticmethod
    def info(msg):
        print(f"  {ColorPrint.BLUE}ℹ️  {msg}{ColorPrint.END}")

    @staticmethod
    def warn(msg):
        print(f"  {ColorPrint.YELLOW}⚠️  {msg}{ColorPrint.END}")

    @staticmethod
    def url(msg):
        print(f"  {ColorPrint.PURPLE}{ColorPrint.BOLD}🌐 {msg}{ColorPrint.END}")


class SilentHandler(http.server.SimpleHTTPRequestHandler):
    """Servidor HTTP silencioso (sin logs molestos en consola)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Solo mostrar errores importantes
        if args and len(args) >= 2:
            status = str(args[1])
            if status.startswith('4') or status.startswith('5'):
                ColorPrint.warn(f"Error {status}: {args[0]}")

    def end_headers(self):
        # Headers para permitir que Three.js y fuentes externas carguen bien
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


def open_browser(url, delay=1.5):
    """Abre el navegador después de un pequeño delay"""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        ColorPrint.ok(f"¡Navegador abierto!")
    except Exception:
        ColorPrint.warn("No se pudo abrir el navegador automáticamente.")


def start_server():
    ColorPrint.banner()

    url = f"http://localhost:{PORT}"

    ColorPrint.info(f"Iniciando servidor en el puerto {PORT}...")
    ColorPrint.info(f"Directorio: {DIRECTORY}")
    print()

    try:
        with socketserver.TCPServer(("", PORT), SilentHandler) as httpd:
            httpd.allow_reuse_address = True

            ColorPrint.ok("¡Servidor iniciado correctamente!")
            ColorPrint.url(f"Abre esta dirección en tu navegador:")
            print(f"\n      👉  {url}  👈\n")
            ColorPrint.info("Abriendo el navegador automáticamente...")
            ColorPrint.info("Presiona Ctrl+C para detener el servidor\n")

            # Abrir navegador en un hilo separado
            t = threading.Thread(target=open_browser, args=(url,), daemon=True)
            t.start()

            print(f"  {ColorPrint.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{ColorPrint.END}")
            print(f"  {ColorPrint.GREEN}  Servidor activo... ¡Disfruta aprendiendo! 🎓{ColorPrint.END}")
            print(f"  {ColorPrint.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{ColorPrint.END}\n")

            httpd.serve_forever()

    except OSError as e:
        if "Address already in use" in str(e):
            ColorPrint.warn(f"El puerto {PORT} ya está en uso.")
            ColorPrint.info(f"Intenta abrir directamente: {url}")
            print(f"\n  O ejecuta: python3 server.py\n")
        else:
            raise e
    except KeyboardInterrupt:
        print(f"\n\n  {ColorPrint.BLUE}👋 ¡Hasta luego! El servidor se ha detenido.{ColorPrint.END}\n")


if __name__ == '__main__':
    start_server()
