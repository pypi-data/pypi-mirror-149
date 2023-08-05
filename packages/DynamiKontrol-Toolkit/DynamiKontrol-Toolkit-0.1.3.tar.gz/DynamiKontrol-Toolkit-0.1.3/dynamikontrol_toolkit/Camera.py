import cv2
import mediapipe as mp

class Face():
    def __init__(self, face_landmarks):
        # face
        left = face_landmarks.landmark[227].x
        right = face_landmarks.landmark[454].x
        upper = face_landmarks.landmark[10].y
        lower = face_landmarks.landmark[152].y
        width = right - left
        height = abs( upper - lower )  

        self.x1 = left
        self.y1 = upper
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

        # lips
        self.lips_left = face_landmarks.landmark[62].x
        self.lips_right = face_landmarks.landmark[292].x
        self.lips_upper = face_landmarks.landmark[13].y
        self.lips_lower = face_landmarks.landmark[14].y
        self.lips_width = self.lips_right - self.lips_left
        self.lips_height = abs( self.lips_upper - self.lips_lower )

        self.lips = Lips( x1 = self.lips_left, y1 = self.lips_upper, width = self.lips_width, height = self.lips_height )

        ##### left eye
        self.left_eye_left = face_landmarks.landmark[33].x
        self.left_eye_right = face_landmarks.landmark[133].x
        self.left_eye_upper = face_landmarks.landmark[159].y
        self.left_eye_lower = face_landmarks.landmark[145].y
        self.left_eye_width = self.left_eye_right-self.left_eye_left
        self.left_eye_height = abs(self.left_eye_upper - self.left_eye_lower)

        self.left_eye = Eye( x1 = self.left_eye_left, y1 = self.left_eye_upper
                        , width = self.left_eye_width, height = self.left_eye_height )

        ##### right eye
        self.right_eye_left = face_landmarks.landmark[362].x
        self.right_eye_right = face_landmarks.landmark[263].x
        self.right_eye_upper = face_landmarks.landmark[386].y
        self.right_eye_lower = face_landmarks.landmark[374].y
        self.right_eye_width = self.right_eye_right-self.right_eye_left
        self.right_eye_height = abs(self.right_eye_upper - self.right_eye_lower)

        self.right_eye = Eye( x1 = self.right_eye_left, y1 = self.right_eye_upper
                        , width = self.right_eye_width, height = self.right_eye_height )

        #### left iris
        # self.left_iris_center = face_landmarks.landmark[468].x
        self.left_iris_right = face_landmarks.landmark[469].x
        self.left_iris_left = face_landmarks.landmark[471].x
        self.left_iris_upper = face_landmarks.landmark[470].y
        self.left_iris_lower = face_landmarks.landmark[472].y
        self.left_iris_width = self.left_iris_right-self.left_iris_left
        self.left_iris_height = abs(self.left_iris_upper - self.left_iris_lower)

        self.left_iris = Iris( x1 = self.left_iris_left, y1 = self.left_iris_upper
                        , width = self.left_iris_width, height = self.left_iris_height )

        #### right iris
        # self.right_iris_center = face_landmarks.landmark[473].x
        self.right_iris_right = face_landmarks.landmark[474].x
        self.right_iris_left = face_landmarks.landmark[476].x
        self.right_iris_upper = face_landmarks.landmark[475].y
        self.right_iris_lower = face_landmarks.landmark[477].y
        self.right_iris_width = self.right_iris_right-self.right_iris_left
        self.right_iris_height = abs(self.right_iris_upper - self.right_iris_lower)

        self.right_iris = Iris( x1 = self.right_iris_left, y1 = self.right_iris_upper
                        , width = self.right_iris_width, height = self.right_iris_height )

    def is_located_left(self):
        return self.center_x <= 0.4
    def is_located_right(self):
        return self.center_x >= 0.6
    def is_located_top(self):
        return self.center_y <= 0.4
    def is_located_bottom(self):
        return self.center_y >= 0.6

    def is_mouth_opened(self, ratio = 0.3 ):
        return (self.lips_height) >= (self.width*ratio)

    def look_left(self, ratio = 0.4):
        look_left = (self.left_iris.center_x <= (self.left_eye.x1 + self.left_eye.width*ratio)) and (self.right_iris.center_x <= (self.right_eye.x1 + self.right_eye.width*ratio))
        return look_left
    def look_right(self, ratio = 0.4):
        look_right = (self.left_iris.center_x >= (self.left_eye.x2 - self.left_eye.width*ratio)) and (self.right_iris.center_x >= (self.right_eye.x2 - self.right_eye.width*ratio))
        return look_right

    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

class Lips():
    def __init__(self,x1,y1,width,height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2
    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

##### Eye
class Eye():
    def __init__(self,x1,y1,width,height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

#### Iris
class Iris():
    def __init__(self,x1,y1,width,height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

class Camera():
    def __init__(self, path:any=0, width:int = None, height:int = None ) -> None:

        self.camera = cv2.VideoCapture(path)

        if width is None or height is None:     
            self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.width = int(width)
            self.height = int(height)

    def is_opened(self, close_key: int or str = 27) -> bool:
        if not self.camera.isOpened():
            return False

        ret, img = self.camera.read()

        if not ret:
            return False

        if len(str(close_key)) == 1:
            close_key = ord(close_key)
            print(close_key)
            if cv2.waitKey(20) & 0xFF == close_key:
                return False
        else:
            if cv2.waitKey(20) & 0xFF == close_key:
                return False

        self.frame = img
        self.frame = cv2.resize(self.frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

        return True

    def get_frame(self, mirror_mode = True):

        if mirror_mode is True:
            self.frame = cv2.flip(self.frame, 1)
        elif mirror_mode is False:
            pass

        return self.frame

    def show(self, frame, window_name = "Window"):
        return cv2.imshow(window_name, frame)

    def draw_faces(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (round(self.width*face.x1), round(self.height*face.y1)),
                    (round(self.width*face.x2),round(self.height*face.y2)),
                    (0,255,0), 3)
    
    def draw_lips(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (round(self.width*face.lips.x1), round(self.height*face.lips.y1)),
                    (round(self.width*face.lips.x2),round(self.height*face.lips.y2)),
                    (0,255,0), 3)

    def draw_eyes(self, faces):
       for face in faces:
            left_eye_c_x = round(face.left_eye.center_x*self.width)
            left_eye_c_y = round(face.left_eye.center_y*self.height)
            left_eye_width = round(face.left_eye.width*0.5*self.width)
            left_eye_height = round(face.left_eye.height*0.5*self.height)

            right_eye_c_x = round(face.right_eye.center_x*self.width)
            right_eye_c_y = round(face.right_eye.center_y*self.height)
            right_eye_width = round(face.right_eye.width*0.5*self.width)
            right_eye_height = round(face.right_eye.height*0.5*self.height)

            left_eye_points = cv2.ellipse2Poly( (left_eye_c_x, left_eye_c_y),(left_eye_width,left_eye_height), 0, 0, 360, 30 )
            self.frame = cv2.polylines( self.frame, [left_eye_points], False, (0,255,0), 2 )

            right_eye_points = cv2.ellipse2Poly( (right_eye_c_x, right_eye_c_y),(right_eye_width,right_eye_height), 0, 0, 360, 30 )
            self.frame = cv2.polylines( self.frame, [right_eye_points], False, (0,255,0), 2 )

    def draw_irides(self, faces):
       for face in faces:
            self.frame = cv2.circle( self.frame, ( round(face.left_iris.center_x*self.width) , round(face.left_iris.center_y*self.height) ),
                                round( min( [self.width, self.height] ) * face.left_iris.width * 0.5 ), (0,255,0), 2 )
            self.frame = cv2.circle( self.frame, ( round(face.right_iris.center_x*self.width) , round(face.right_iris.center_y*self.height) ),
                                round( min( [self.width, self.height] ) * face.right_iris.width * 0.5 ), (0,255,0), 2 )

    def detect_face(self, frame, max_num_face = 1 , draw_face = True, draw_lips = True, draw_eyes = True, draw_irides = True) -> object or None:

        mp_face_mesh = mp.solutions.face_mesh

        face = []

        with mp_face_mesh.FaceMesh(
            max_num_faces=max_num_face,
            refine_landmarks=True,
            min_detection_confidence=0.4, 
            min_tracking_confidence=0.5) as face_mesh:

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:  
                        face.append( Face(face_landmarks) )

        if draw_face:
            self.draw_faces(face)
        if draw_lips:
            self.draw_lips(face)
        if draw_eyes:
            self.draw_eyes(face)
        if draw_irides:
            self.draw_irides(face)

        if len(face) == 1 and max_num_face == 1:
            return face[0]

        return None

    def detect_faces(self, frame, max_num_faces = 99, draw_faces =True, draw_lips = True, draw_eyes = True, draw_irides = True) -> list:
 
        mp_face_mesh = mp.solutions.face_mesh

        faces = []

        with mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=0.4, 
            min_tracking_confidence=0.5) as face_mesh:

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:  
                        faces.append( Face(face_landmarks) )

        if draw_faces:
            self.draw_faces(faces)
        if draw_lips:
            self.draw_lips(faces)
        if draw_eyes:
            self.draw_eyes(faces)
        if draw_irides:
            self.draw_irides(faces)

        return faces




