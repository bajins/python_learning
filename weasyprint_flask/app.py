import io
from flask import Flask, request, render_template, Response, flash, redirect, url_for
from weasyprint import HTML
# 确保已安装 xhtml2pdf: pip install xhtml2pdf
from xhtml2pdf import pisa

# 初始化 Flask 应用
app = Flask(__name__)
# 设置一个密钥，用于 flash 消息，这对于生产环境很重要
app.secret_key = 'a_very_secret_key'


def convert_weasyprint(html_content: str) -> bytes:
    """
    使用 WeasyPrint 将 HTML 字符串转换为 PDF。
    :param html_content: HTML内容的字符串。
    :return: PDF 的二进制数据。
    """
    # WeasyPrint 直接处理 HTML 字符串，并在内存中生成 PDF
    return HTML(string=html_content).write_pdf()


def convert_xhtml2pdf(html_content: str) -> bytes:
    """
    使用 xhtml2pdf 将 HTML 字符串转换为 PDF。
    :param html_content: HTML内容的字符串。
    :return: PDF 的二进制数据。
    """
    # 创建一个 BytesIO 对象，用于在内存中保存 PDF 文件
    result = io.BytesIO()

    # 调用 pisa.CreatePDF 来转换 HTML
    # - 第一个参数是源HTML，可以是字符串或文件对象
    # - 第二个参数是目标PDF，一个可写的文件类对象
    pdf = pisa.CreatePDF(
        src=io.StringIO(html_content),  # 将HTML字符串封装成文件类对象
        dest=result
    )

    # 检查转换是否成功，如果失败则抛出异常
    if pdf.err:
        raise Exception(f"xhtml2pdf conversion error: {pdf.err}")
    
    # 从 BytesIO 对象中获取 PDF 数据并返回
    return result.getvalue()


# 为同一个 URL 定义 GET 和 POST 方法
@app.route('/', methods=['GET', 'POST'])
def upload_and_convert():
    # 如果是 POST 请求（用户提交了表单）
    if request.method == 'POST':
        # 1. 检查请求中是否包含文件部分
        if 'html_file' not in request.files:
            flash('请求中没有文件部分 (No file part in the request.)')
            return redirect(request.url)
        
        file = request.files['html_file']

        # 2. 检查用户是否选择了文件
        if file.filename == '':
            flash('未选择任何文件 (No file selected.)')
            return redirect(request.url)

        # 3. 确保文件是 HTML 文件并且存在
        if file and file.filename.endswith('.html'):
            try:
                # 4. 读取上传文件的内容
                # file.read() 返回的是 bytes，需要解码成 utf-8 字符串
                html_content = file.read().decode('utf-8')
                
                # 5. 根据用户在表单中的选择，决定使用哪个转换器
                converter_choice = request.form.get('converter', 'weasyprint') # 默认为 weasyprint

                if converter_choice == 'weasyprint':
                    flash('使用 WeasyPrint 进行转换...', 'info')
                    pdf_bytes = convert_weasyprint(html_content)
                elif converter_choice == 'xhtml2pdf':
                    flash('使用 xhtml2pdf 进行转换...', 'info')
                    pdf_bytes = convert_xhtml2pdf(html_content)
                else:
                    # 如果收到无效的转换器名称，则报错
                    flash(f'无效的转换器: {converter_choice}', 'error')
                    return redirect(request.url)
                
                
                # 6. 创建一个 HTTP 响应，将 PDF 发送给用户
                return Response(
                    pdf_bytes,
                    mimetype='application/pdf',
                    headers={
                        # 让浏览器弹出下载对话框，并命名文件
                        'Content-Disposition': 'attachment;filename=converted_document.pdf'
                    }
                )
            except Exception as e:
                # 捕获转换过程中可能出现的任何错误
                flash(f"PDF 转换过程中发生错误: {e}", 'error')
                return redirect(request.url)
        else:
            flash('文件类型无效，请上传 HTML 文件。 (Invalid file type.)')
            return redirect(request.url)

    # 如果是 GET 请求，只渲染上传页面
    return render_template('upload.html')


# 定义一个路由，只接受 POST 请求
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # 从请求体中获取 HTML 内容
    # request.data 是二进制数据，需要解码为 utf-8 字符串
    html_content = request.data.decode('utf-8')

    if not html_content:
        return "请求体中未提供 HTML 内容 (No HTML content provided in the request body.)", 400

    try:
        # 默认使用 WeasyPrint 将 HTML 字符串转换为 PDF
        pdf_bytes = convert_weasyprint(html_content)

        # 创建一个 HTTP 响应
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                # 这个头信息会让浏览器弹出下载对话框，而不是直接显示 PDF
                'Content-Disposition': 'attachment;filename=generated_report.pdf'
            }
        )
    except Exception as e:
        return f"发生错误 (An error occurred): {e}", 500


if __name__ == '__main__':
    # 使用 0.0.0.0 可以让局域网内的其他设备访问
    # debug=True 会在代码更改后自动重载，但请勿在生产环境中使用
    app.run(host='0.0.0.0', port=8080, debug=True)