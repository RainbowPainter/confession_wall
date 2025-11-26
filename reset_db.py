import os
import shutil


def reset_database():
    # 删除数据库文件
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("✅ 已删除数据库文件")

    # 删除迁移文件（保留 __init__.py）
    migrations_dir = 'confession/migrations'
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file != '__init__.py' and file.endswith('.py'):
                os.remove(os.path.join(migrations_dir, file))
        print("✅ 已清理迁移文件")

    print("🎯 现在请运行以下命令：")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    print("python manage.py createsuperuser")


if __name__ == '__main__':
    reset_database()