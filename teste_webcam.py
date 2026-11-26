
import cv2
from pathlib import Path

# ==========================================
# 1. CONFIGURAR O DETECTOR FACIAL
# ==========================================

caminho_detector = Path(
    r"C:\FaceAccessModelos\haarcascade_frontalface_default.xml"
)

if not caminho_detector.is_file():
    raise FileNotFoundError(
        f"Arquivo do detector nao encontrado: {caminho_detector}"
    )

detector = cv2.CascadeClassifier(str(caminho_detector))

if detector.empty():
    raise RuntimeError(
        "Nao foi possivel carregar o detector facial."
    )

print("Detector facial carregado com sucesso!")


# ==========================================
# 2. INICIAR A WEBCAM
# ==========================================

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("ERRO: Nao foi possivel abrir a webcam.")
    raise SystemExit(1)

print("Webcam iniciada!")
print("Pressione Q para encerrar.")


# ==========================================
# 3. DETECTAR ROSTOS EM TEMPO REAL
# ==========================================

try:
    while True:
        sucesso, imagem = camera.read()

        if not sucesso:
            print("Erro ao capturar imagem.")
            break

        cinza = cv2.cvtColor(
            imagem,
            cv2.COLOR_BGR2GRAY
        )

        rostos = detector.detectMultiScale(
            cinza,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        for x, y, largura, altura in rostos:
            # Desenhar retangulo verde
            cv2.rectangle(
                imagem,
                (x, y),
                (x + largura, y + altura),
                (0, 255, 0),
                2
            )

            # Exibir mensagem acima do rosto
            cv2.putText(
                imagem,
                "ROSTO DETECTADO",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "FaceAccess - Teste da Webcam",
            imagem
        )

        # Pressionar Q para encerrar
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()

print("Webcam encerrada.")
