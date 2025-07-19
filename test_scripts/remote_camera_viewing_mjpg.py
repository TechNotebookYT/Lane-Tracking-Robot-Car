import cv2
import time
import threading
import http.server
import socketserver
import io
import sys
import numpy as np

# --- Configuration ---
CAMERA_INDEX = 0  # Typically 0 for the first webcam. Adjust if you have multiple.
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
JPEG_QUALITY = 70 # JPEG compression quality (0-100), higher means larger file/better quality
SERVER_PORT = 8000 # Port to serve the MJPEG stream on

# Global variable to hold the latest JPEG frame
latest_frame = None
# Lock to protect the latest_frame variable from concurrent access
frame_lock = threading.Lock()

class StreamingHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            try:
                while True:
                    with frame_lock:
                        if latest_frame is not None:
                            # Create a byte array for the JPEG image
                            self.wfile.write(b'--frame\r\n')
                            self.send_header('Content-Type', 'image/jpeg')
                            self.send_header('Content-Length', str(len(latest_frame)))
                            self.end_headers()
                            self.wfile.write(latest_frame)
                            self.wfile.write(b'\r\n')
                        else:
                            # If no frame yet, wait a bit
                            time.sleep(0.1)
            except Exception as e:
                # Log client disconnection or other errors
                sys.stderr.write(f"Client disconnected or error: {e}\n")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found. Access /stream.mjpg for the video feed.")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""
    pass

def capture_frames():
    """Captures frames from the webcam and updates the global latest_frame."""
    global latest_frame
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        sys.stderr.write(f"Error: Could not open webcam with index {CAMERA_INDEX}\n")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    sys.stderr.write(f"Capturing frames from webcam (Resolution: {FRAME_WIDTH}x{FRAME_HEIGHT})...\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                sys.stderr.write("Error: Could not read frame from webcam. Retrying...\n")
                time.sleep(1) # Wait before retrying
                continue

            # Convert to grayscale to reduce data size and potential delay
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Encode grayscale frame as JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY] # JPEG quality for grayscale
            result, encoded_image = cv2.imencode('.jpg', gray_frame, encode_param)

            if not result:
                sys.stderr.write("Error: Could not encode frame as JPEG.\n")
                continue

            with frame_lock:
                latest_frame = encoded_image.tobytes()

            # Optional: control frame rate by adding a sleep here
            time.sleep(1/15) # ~15 FPS

    except KeyboardInterrupt:
        sys.stderr.write("\nFrame capture stopped.\n")
    except Exception as e:
        sys.stderr.write(f"Error in capture_frames: {e}\n")
    finally:
        cap.release()
        sys.stderr.write("Webcam released.\n")

if __name__ == "__main__":
    sys.stderr.write("Starting MJPEG Webcam Stream Server...\n")

    # Start the frame capture in a separate thread
    capture_thread = threading.Thread(target=capture_frames)
    capture_thread.daemon = True # Allow the main program to exit even if this thread is running
    capture_thread.start()

    # Wait a moment for the camera to initialize and capture the first frame
    time.sleep(2)

    # Start the HTTP server
    try:
        server = ThreadedHTTPServer(("", SERVER_PORT), StreamingHandler)
        sys.stderr.write(f"Server started on port {SERVER_PORT}. Access http://<Your_Pi_IP>:{SERVER_PORT}/stream.mjpg\n")
        server.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\nServer stopped by user.\n")
    except Exception as e:
        sys.stderr.write(f"Error starting server: {e}\n")
    finally:
        sys.stderr.write("Shutting down.\n")
        # In a real application, you might want to signal capture_thread to stop gracefully
        # For a test script, daemon=True will let it exit with the main process.