<<<<<<< HEAD
# filter.py
"""
Main logic for the interactive TikTok-style quiz filter with head tracking.
"""

# Impor pustaka OpenCV dan time untuk pengolahan video dan timing
import cv2
import time

# Impor fungsi eksternal dari modul yang berbeda
from question_bank import get_random_question              # Mengambil soal acak
from video_utils import HeadTracker, overlay_question, overlay_score  # Utilitas video: pelacakan kepala dan tampilan overlay
from audio_utils import play_sound_effect                 # Memainkan efek suara

def animate_transition(frame, text, duration=1.0, font_scale=0.6):
    """
    Menampilkan transisi teks dengan efek fade in/out.
    """
    if frame is None:
        return False

    h, w, _ = frame.shape               # Ambil dimensi frame
    start_time = time.time()
    frame_time = 1/60                  # Asumsikan 60 FPS

    while (time.time() - start_time) < duration:
        # Hitung alpha (transparansi) untuk blending transisi
        alpha = min(1.0, (time.time() - start_time) / (duration * 0.5))
        if time.time() - start_time > duration * 0.5:
            alpha = 1.0 - (time.time() - start_time - duration * 0.5) / (duration * 0.5)

        overlay = frame.copy()
        # Gambar kotak latar belakang teks
        cv2.rectangle(overlay, (w//2-250, h//2-40), (w//2+250, h//2+40), (255,255,255), -1)
        
        # Hitung posisi teks agar terpusat
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        textX = w//2 - textsize[0]//2
        # Gambar teks ke overlay
        cv2.putText(overlay, text, (textX, h//2+10), 
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), 2)
        # Gabungkan overlay dan frame dengan alpha
        blend = cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0)
        cv2.imshow('Filter Informatika', blend)

        # Tunggu sebentar untuk memberi waktu render
        wait_time = max(1, int(frame_time * 1000))
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            return False
    return True

def show_preparation(cap, countdown_time=3):
    """
    Menampilkan countdown sebelum pertanyaan berikutnya.
    """
    start_time = time.time()
    frame_time = 1/30
    last_second = countdown_time

    while time.time() - start_time < countdown_time:
        current_time = time.time() - start_time
        current_second = countdown_time - int(current_time)

        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)  # Cermin horizontal agar tampak seperti kamera depan

        if current_second != last_second:
            last_second = current_second
        text = f"Bersiap untuk soal berikutnya... {current_second}"

        # Gambar kotak putih dan teks countdown
        h, w, _ = frame.shape
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//2-250, h//2-40), (w//2+250, h//2+40), (255,255,255), -1)
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        textX = w//2 - textsize[0]//2
        cv2.putText(overlay, text, (textX, h//2+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

        alpha = 0.7
        blend = cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0)
        cv2.imshow('Filter Informatika', blend)

        wait_time = max(1, int(frame_time * 1000))
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            return False
    return True

def run_filter():
    """
    Fungsi utama yang menjalankan kuis dengan deteksi arah kepala dan skor.
    """
    cap = cv2.VideoCapture(0)     # Akses webcam
    if not cap.isOpened():
        print("Error: Tidak dapat mengakses kamera")
        return

    # Set resolusi kamera dan frame rate
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    score = 0
    total_questions = 5
    current_question = 0
    head_tracker = HeadTracker()  # Inisialisasi pelacak arah kepala
    frame_time = 1/30

    ret, frame = cap.read()
    if ret:
        h, w, _ = frame.shape
    else:
        h, w = 480, 640  # fallback

    # Konfigurasi deteksi pose
    last_pose = None
    pose_confirmation_frames = 0
    required_confirmation_frames = 10  # Lebih responsif
    pose_history = []
    history_length = 15
    stable_pose_threshold = 0.75  # 75% stabilitas pose

    min_answer_time = 1.5  # Minimal waktu sebelum jawaban bisa diberikan

    # Tampilkan ucapan selamat datang
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        animate_transition(frame, "Selamat Datang!", 4.0, font_scale=0.6)

    # Loop soal
    while current_question < total_questions:
        question_data = get_random_question()
        question = question_data['question']
        option_a = question_data['option_b']
        option_b = question_data['option_a']
        correct_answer = question_data['answer']

        question_start = time.time()
        question_duration = 20
        answered = False
        last_pose_check = 0
        pose_check_interval = 0.1
        pose_history.clear()

        last_pose = None
        pose_confirmation_frames = 0
        answer_ready = False

        while time.time() - question_start < question_duration and not answered:
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            current_time = time.time()

            if current_time - question_start >= min_answer_time:
                answer_ready = True

            if current_time - last_pose_check >= pose_check_interval and answer_ready:
                current_pose = head_tracker.get_head_pose(frame)
                last_pose_check = current_time

                if current_pose in ['left', 'right']:
                    pose_history.append(current_pose)
                    if len(pose_history) > history_length:
                        pose_history.pop(0)
                    if current_pose == last_pose:
                        pose_confirmation_frames += 1
                    else:
                        pose_confirmation_frames = max(0, pose_confirmation_frames - 1)
                else:
                    pose_confirmation_frames = max(0, pose_confirmation_frames - 1)

                last_pose = current_pose

                if len(pose_history) >= history_length:
                    left_count = pose_history.count('left')
                    right_count = pose_history.count('right')
                    max_count = max(left_count, right_count)
                    pose_consistency = max_count / len(pose_history)

                    if pose_confirmation_frames >= required_confirmation_frames and pose_consistency >= stable_pose_threshold:
                        if current_pose == 'left' and left_count > right_count:
                            answered = True
                            is_correct = correct_answer == 'A'
                            play_sound_effect(is_correct)
                            if is_correct:
                                score += 1
                            animate_transition(frame, 'Benar!' if is_correct else 'Salah!', 1.0, font_scale=0.8)

                        elif current_pose == 'right' and right_count > left_count:
                            answered = True
                            is_correct = correct_answer == 'B'
                            play_sound_effect(is_correct)
                            if is_correct:
                                score += 1
                            animate_transition(frame, 'Benar!' if is_correct else 'Salah!', 1.0, font_scale=0.8)

            if not answer_ready:
                waiting_text = "Bersiap..."
                cv2.putText(frame, waiting_text, (w//2-50, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                if last_pose in ['left', 'right']:
                    pose_text = f"Pose: {last_pose.upper()}"
                    cv2.putText(frame, pose_text, (w//2-50, h-30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    progress = min(1.0, pose_confirmation_frames / required_confirmation_frames)
                    progress_width = int(100 * progress)
                    cv2.rectangle(frame, (w//2-50, h-15), (w//2-50 + progress_width, h-10), 
                                  (0, 255, 0), -1)

            # Tampilkan pertanyaan dan jawaban
            frame = overlay_question(frame, question, option_a, option_b, head_tracker)

            # Tampilkan timer
            remaining = int(question_duration - (current_time - question_start))
            cv2.putText(frame, str(remaining), (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow('Filter Informatika', frame)
            wait_time = max(1, int(frame_time * 1000))
            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                break

        current_question += 1

        if current_question < total_questions:
            show_preparation(cap)

    # Tampilkan skor akhir
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        animate_transition(frame, f"Permainan Selesai!\nSkor Anda: {score}/{total_questions}", 2.0, font_scale=0.8)
        frame = overlay_score(frame, score, total_questions)
        cv2.imshow('Filter Informatika', frame)
        cv2.waitKey(3000)

    # Bersihkan sumber daya
    cap.release()
    cv2.destroyAllWindows()
=======
# filter.py
"""
Main logic for the interactive TikTok-style quiz filter with head tracking.
"""

# Impor pustaka OpenCV dan time untuk pengolahan video dan timing
import cv2
import time

# Impor fungsi eksternal dari modul yang berbeda
from question_bank import get_random_question              # Mengambil soal acak
from video_utils import HeadTracker, overlay_question, overlay_score  # Utilitas video: pelacakan kepala dan tampilan overlay
from audio_utils import play_sound_effect                 # Memainkan efek suara

def animate_transition(frame, text, duration=1.0, font_scale=0.6):
    """
    Menampilkan transisi teks dengan efek fade in/out.
    """
    if frame is None:
        return False

    h, w, _ = frame.shape               # Ambil dimensi frame
    start_time = time.time()
    frame_time = 1/60                  # Asumsikan 60 FPS

    while (time.time() - start_time) < duration:
        # Hitung alpha (transparansi) untuk blending transisi
        alpha = min(1.0, (time.time() - start_time) / (duration * 0.5))
        if time.time() - start_time > duration * 0.5:
            alpha = 1.0 - (time.time() - start_time - duration * 0.5) / (duration * 0.5)

        overlay = frame.copy()
        # Gambar kotak latar belakang teks
        cv2.rectangle(overlay, (w//2-250, h//2-40), (w//2+250, h//2+40), (255,255,255), -1)
        
        # Hitung posisi teks agar terpusat
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        textX = w//2 - textsize[0]//2
        # Gambar teks ke overlay
        cv2.putText(overlay, text, (textX, h//2+10), 
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), 2)
        # Gabungkan overlay dan frame dengan alpha
        blend = cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0)
        cv2.imshow('Filter Informatika', blend)

        # Tunggu sebentar untuk memberi waktu render
        wait_time = max(1, int(frame_time * 1000))
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            return False
    return True

def show_preparation(cap, countdown_time=3):
    """
    Menampilkan countdown sebelum pertanyaan berikutnya.
    """
    start_time = time.time()
    frame_time = 1/30
    last_second = countdown_time

    while time.time() - start_time < countdown_time:
        current_time = time.time() - start_time
        current_second = countdown_time - int(current_time)

        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)  # Cermin horizontal agar tampak seperti kamera depan

        if current_second != last_second:
            last_second = current_second
        text = f"Bersiap untuk soal berikutnya... {current_second}"

        # Gambar kotak putih dan teks countdown
        h, w, _ = frame.shape
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//2-250, h//2-40), (w//2+250, h//2+40), (255,255,255), -1)
        textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        textX = w//2 - textsize[0]//2
        cv2.putText(overlay, text, (textX, h//2+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

        alpha = 0.7
        blend = cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0)
        cv2.imshow('Filter Informatika', blend)

        wait_time = max(1, int(frame_time * 1000))
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            return False
    return True

def run_filter():
    """
    Fungsi utama yang menjalankan kuis dengan deteksi arah kepala dan skor.
    """
    cap = cv2.VideoCapture(0)     # Akses webcam
    if not cap.isOpened():
        print("Error: Tidak dapat mengakses kamera")
        return

    # Set resolusi kamera dan frame rate
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    score = 0
    total_questions = 5
    current_question = 0
    head_tracker = HeadTracker()  # Inisialisasi pelacak arah kepala
    frame_time = 1/30

    ret, frame = cap.read()
    if ret:
        h, w, _ = frame.shape
    else:
        h, w = 480, 640  # fallback

    # Konfigurasi deteksi pose
    last_pose = None
    pose_confirmation_frames = 0
    required_confirmation_frames = 10  # Lebih responsif
    pose_history = []
    history_length = 15
    stable_pose_threshold = 0.75  # 75% stabilitas pose

    min_answer_time = 1.5  # Minimal waktu sebelum jawaban bisa diberikan

    # Tampilkan ucapan selamat datang
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        animate_transition(frame, "Selamat Datang!", 4.0, font_scale=0.6)

    # Loop soal
    while current_question < total_questions:
        question_data = get_random_question()
        question = question_data['question']
        option_a = question_data['option_b']
        option_b = question_data['option_a']
        correct_answer = question_data['answer']

        question_start = time.time()
        question_duration = 20
        answered = False
        last_pose_check = 0
        pose_check_interval = 0.1
        pose_history.clear()

        last_pose = None
        pose_confirmation_frames = 0
        answer_ready = False

        while time.time() - question_start < question_duration and not answered:
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            current_time = time.time()

            if current_time - question_start >= min_answer_time:
                answer_ready = True

            if current_time - last_pose_check >= pose_check_interval and answer_ready:
                current_pose = head_tracker.get_head_pose(frame)
                last_pose_check = current_time

                if current_pose in ['left', 'right']:
                    pose_history.append(current_pose)
                    if len(pose_history) > history_length:
                        pose_history.pop(0)
                    if current_pose == last_pose:
                        pose_confirmation_frames += 1
                    else:
                        pose_confirmation_frames = max(0, pose_confirmation_frames - 1)
                else:
                    pose_confirmation_frames = max(0, pose_confirmation_frames - 1)

                last_pose = current_pose

                if len(pose_history) >= history_length:
                    left_count = pose_history.count('left')
                    right_count = pose_history.count('right')
                    max_count = max(left_count, right_count)
                    pose_consistency = max_count / len(pose_history)

                    if pose_confirmation_frames >= required_confirmation_frames and pose_consistency >= stable_pose_threshold:
                        if current_pose == 'left' and left_count > right_count:
                            answered = True
                            is_correct = correct_answer == 'A'
                            play_sound_effect(is_correct)
                            if is_correct:
                                score += 1
                            animate_transition(frame, 'Benar!' if is_correct else 'Salah!', 1.0, font_scale=0.8)

                        elif current_pose == 'right' and right_count > left_count:
                            answered = True
                            is_correct = correct_answer == 'B'
                            play_sound_effect(is_correct)
                            if is_correct:
                                score += 1
                            animate_transition(frame, 'Benar!' if is_correct else 'Salah!', 1.0, font_scale=0.8)

            if not answer_ready:
                waiting_text = "Bersiap..."
                cv2.putText(frame, waiting_text, (w//2-50, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                if last_pose in ['left', 'right']:
                    pose_text = f"Pose: {last_pose.upper()}"
                    cv2.putText(frame, pose_text, (w//2-50, h-30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    progress = min(1.0, pose_confirmation_frames / required_confirmation_frames)
                    progress_width = int(100 * progress)
                    cv2.rectangle(frame, (w//2-50, h-15), (w//2-50 + progress_width, h-10), 
                                  (0, 255, 0), -1)

            # Tampilkan pertanyaan dan jawaban
            frame = overlay_question(frame, question, option_a, option_b, head_tracker)

            # Tampilkan timer
            remaining = int(question_duration - (current_time - question_start))
            cv2.putText(frame, str(remaining), (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow('Filter Informatika', frame)
            wait_time = max(1, int(frame_time * 1000))
            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                break

        current_question += 1

        if current_question < total_questions:
            show_preparation(cap)

    # Tampilkan skor akhir
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        animate_transition(frame, f"Permainan Selesai!\nSkor Anda: {score}/{total_questions}", 2.0, font_scale=0.8)
        frame = overlay_score(frame, score, total_questions)
        cv2.imshow('Filter Informatika', frame)
        cv2.waitKey(3000)

    # Bersihkan sumber daya
    cap.release()
    cv2.destroyAllWindows()
>>>>>>> 3d16b93 (integrasi feed kamera dan styling elemen UI)
