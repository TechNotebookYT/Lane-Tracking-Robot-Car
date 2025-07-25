import cv2
import time
import threading
import http.server
import socketserver
import numpy as np
import sys

class ImageStreamer:
    """
    A class that manages a threaded HTTP server to stream images.
    The image being streamed can be updated by calling the update_image method.
    """
    def __init__(self, port=8000, jpeg_quality=70):
        """
        Initializes the streamer.
        Args:
            port (int): The port to serve the MJPEG stream on.
            jpeg_quality (int): The JPEG compression quality (0-100).
        """
        self.port = port
        self.jpeg_quality = jpeg_quality
        self.latest_frame_bytes = None
        self.frame_lock = threading.Lock()
        self.server_thread = None
        self.http_server = None

    def _create_handler_class(self):
        """Creates a request handler class that has access to this streamer instance."""
        streamer_instance = self

        class StreamingHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/stream.mjpg':
                    self.send_response(200)
                    self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
                    self.end_headers()
                    try:
                        while True:
                            with streamer_instance.frame_lock:
                                if streamer_instance.latest_frame_bytes:
                                    frame = streamer_instance.latest_frame_bytes
                                else:
                                    # If no frame yet, wait a bit and continue
                                    time.sleep(0.1)
                                    continue

                            self.wfile.write(b'--frame\r\n')
                            self.send_header('Content-Type', 'image/jpeg')
                            self.send_header('Content-Length', str(len(frame)))
                            self.end_headers()
                            self.wfile.write(frame)
                            self.wfile.write(b'\r\n')
                            time.sleep(1/30) # Limit frame rate to ~30 FPS
                    except Exception as e:
                        # Client disconnected or another error occurred
                        sys.stderr.write(f"Client disconnected or error: {e}\n")
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found. Access /stream.mjpg for the video feed.")
        
        return StreamingHandler

    def update_image(self, numpy_frame):
        """
        Updates the image to be streamed.
        Args:
            numpy_frame (np.ndarray): The new image frame (from OpenCV).
        """
        if numpy_frame is None:
            return

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
        result, encoded_image = cv2.imencode('.jpg', numpy_frame, encode_param)

        if not result:
            sys.stderr.write("Error: Could not encode frame as JPEG.\n")
            return

        with self.frame_lock:
            self.latest_frame_bytes = encoded_image.tobytes()

    def start(self):
        """Starts the HTTP server in a separate thread."""
        class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
            """Handle requests in a separate thread."""
            pass

        handler_class = self._create_handler_class()
        self.http_server = ThreadedHTTPServer(("", self.port), handler_class)
        
        self.server_thread = threading.Thread(target=self.http_server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        sys.stderr.write(f"Image streamer started. Access at: http://<your_ip_address>:{self.port}/stream.mjpg\n")
        
    def stop(self):
        """Stops the HTTP server."""
        if self.http_server:
            self.http_server.shutdown()
            self.http_server.server_close()
            sys.stderr.write("Image streamer stopped.\n")

def main():
    """Main function to demonstrate the ImageStreamer."""
    streamer = ImageStreamer(port=8000)
    streamer.start()

    # --- DEMO 1: Update with dynamically generated images ---
    print("\n--- Starting Demo 1: Generated Text Images ---")
    print("Streaming text images for 10 seconds...")
    width, height = 640, 480
    for i in range(100):
        # Create a black image
        blank_frame = np.zeros((height, width, 3), np.uint8)
        
        # Add text
        text = f"Frame {i+1}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 2, 3)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        cv2.putText(blank_frame, text, (text_x, text_y), font, 2, (0, 255, 0), 3)

        # Update the streamer with the new frame
        streamer.update_image(blank_frame)
        time.sleep(0.1) # Update 10 times per second

    # --- DEMO 2: Update with webcam feed ---
    print("\n--- Starting Demo 2: Webcam Feed ---")
    print("Streaming from webcam. Press Ctrl+C to stop.")
    cap = cv2.VideoCapture(0) # Use camera index 0
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        streamer.stop()
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break
            
            # The magic is here: just call update_image with the webcam frame
            streamer.update_image(frame)
            
            # A small delay is added in the handler, so no sleep is needed here for FPS control
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        cap.release()
        streamer.stop()


if __name__ == "__main__":
    main()