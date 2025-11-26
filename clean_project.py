import os
import shutil


def clean_project():
    # 1. 删除数据库
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("✅ 已删除数据库文件")

    # 2. 清理迁移文件
    migrations_dir = 'confession/migrations'
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file != '__init__.py' and file.endswith('.py'):
                os.remove(os.path.join(migrations_dir, file))
        print("✅ 已清理迁移文件")

    # 3. 清理媒体文件（可选）
    if os.path.exists('media'):
        shutil.rmtree('media')
        os.makedirs('media/confessions', exist_ok=True)
        print("✅ 已清理媒体文件")

    # 4. 清理缓存
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
    print("✅ 已清理缓存文件")

    print("\n🎯 项目已重置！现在运行：")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
    print("4. python manage.py runserver")


if __name__ == '__main__':
    clean_project()