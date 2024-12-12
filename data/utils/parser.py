import os
import sys

import yaml


class DotenvParser:
    def _is_valid_key_value_line(self, line: str):
        if not line:
            return False

        if line.startswith("#"):
            return False

        if '=' not in line:
            return False

        return True

    def parse_env_file(self, env_file_path: str):
        key_value_dict = {}

        with open(env_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if not self._is_valid_key_value_line(line):
                    continue

                key, value = line.split('=', 1)  # 등호 '='로만 분리
                key_value_dict[key.strip()] = value.strip()

        return key_value_dict

    def save_to_yaml(self, env_data: dict[str, str], env_yaml_file_path: str):
        with open(env_yaml_file_path, 'w', encoding='utf-8') as file:
            yaml.dump(env_data, file, default_flow_style=False)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: 스크립트 실행 시 Dotenv 파일을 인자로 제공해야 합니다.')
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f'Error: Dotenv 파일 {sys.argv[1]}가 존재하지 않거나 비정상적인 파일입니다.')
        sys.exit(1)

    dotenv_handler = DotenvParser()

    data = dotenv_handler.parse_env_file(sys.argv[1])
    dotenv_handler.save_to_yaml(data, f'{sys.argv[1]}.yaml')
