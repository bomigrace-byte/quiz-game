import os
import shutil
from datetime import datetime


class BackupManager:
    """state.json의 백업 생성, 백업 목록 조회, 복구 로그 기록을 담당하는 클래스"""

    MAX_BACKUPS = 5  # 보관할 정상 백업 개수 (오래된 것부터 자동 삭제)

    def __init__(self, state_file):
        self.state_file = state_file
        project_dir = os.path.dirname(state_file)
        self.backup_dir = os.path.join(project_dir, "backups")
        self.log_file = os.path.join(self.backup_dir, "recovery.log")

    def _timestamp(self):
        """백업 파일 이름에 붙일 시간 문자열 (예: 20261117_203105)"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _copy_to_backup(self, prefix):
        """state.json을 backups 폴더에 '접두어_시간.json' 이름으로 복사한다.
        성공하면 백업 파일 경로를, 실패하거나 원본이 없으면 None을 반환한다."""
        if not os.path.exists(self.state_file):
            return None
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            backup_path = os.path.join(self.backup_dir, f"{prefix}_{self._timestamp()}.json")
            shutil.copy2(self.state_file, backup_path)
            return backup_path
        except OSError:
            return None

    def create_backup(self):
        """저장하기 직전에 현재 state.json을 백업하고, 오래된 백업을 정리한다."""
        backup_path = self._copy_to_backup("state")
        if backup_path is not None:
            self._remove_old_backups()
        return backup_path

    def backup_corrupted(self):
        """손상된 state.json을 덮어쓰기 전에 원인 확인용으로 따로 보관한다."""
        return self._copy_to_backup("corrupted")

    def list_backups(self):
        """정상 백업 파일 경로 목록을 최신순으로 반환한다."""
        try:
            names = os.listdir(self.backup_dir)
        except OSError:
            return []
        backups = [name for name in names if name.startswith("state_") and name.endswith(".json")]
        backups.sort(reverse=True)  # 이름에 시간이 들어 있어서 이름순 정렬 = 시간순 정렬
        return [os.path.join(self.backup_dir, name) for name in backups]

    def _remove_old_backups(self):
        """정상 백업이 MAX_BACKUPS개를 넘으면 오래된 것부터 삭제한다."""
        for old_path in self.list_backups()[self.MAX_BACKUPS:]:
            try:
                os.remove(old_path)
            except OSError:
                pass

    def write_log(self, message):
        """복구 기록을 backups/recovery.log에 한 줄씩 추가한다."""
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_file, "a", encoding="utf-8") as f:  # "a": 기존 내용 뒤에 추가
                f.write(f"[{now}] {message}\n")
        except OSError:
            pass
