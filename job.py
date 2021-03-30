class Job:
  def __init__(self, browser):
    self.browser = browser
    
  def start(self, business_no, cert_path, cert_pw, do_extract=True):
    self.step_login(business_no, cert_path, cert_pw)
    result = self.step_extract() if do_extract == True else {}
    return result
  
  def wait_for(self, s):
    import time
    el = None
    while el == None:
      try:
        el = self.browser.find_element_by_css_selector(s)
      except:
        el = None
        time.sleep(1)
    return el

  def step_login(self, business_no, cert_path, cert_pw):
    import time
    seqs = (
      ('#txtRegNo1', business_no[:3]),
      ('#txtRegNo2', business_no[3:5]),
      ('#txtRegNo3', business_no[5:]),
    )
    self.browser.get('https://si4n.nhis.or.kr/jpba/JpBaa00101.do')
    [self.browser.find_element_by_css_selector(s).send_keys(k) for s, k in seqs]
    self.browser.execute_script("fn_makeSignNEW('1');")
    btn = self.wait_for('#xwup_media_memorystorage')
    time.sleep(5)
    btn.click()
    file = self.wait_for('#xwup_openFile')
    file.send_keys(cert_path)
    self.browser.execute_script(f"document.querySelectorAll('#xwup_inputpasswd_tek_input1')[0].value = '{cert_pw}'")
    self.browser.find_element_by_css_selector('#xwup_ok').click()

  def alert(self, message):
    import win32api
    win32api.MessageBox(0, message, '')

  def prompt(self, message):
    import pywin.mfc.dialog
    return pywin.mfc.dialog.GetSimpleInput(message)

  def step_extract(self):
    def proc(browser, insu):
      try:
        browser.get('https://si4n.nhis.or.kr/jpbb/JpBba00101.do')
        browser.find_element_by_css_selector('input#insuGubun1').click()
        browser.find_element_by_css_selector(f'input#{insu}').click()
        browser.find_element_by_css_selector('.btn_form01').click()
        browser.implicitly_wait(2)
        browser.find_element_by_css_selector('#allCheck').click()
        browser.execute_script("fn_submit('5')")
        browser.implicitly_wait(2)
        browser.execute_script("document.querySelectorAll('#bankCd')[0].value = '081'")
        browser.execute_script("$('#loading').val('Y');document.frm.submit()")
        browser.implicitly_wait(2)
        price = browser.find_element_by_css_selector('.box_total').text
        account = browser.find_element_by_css_selector('.t_type02.mt20 tr:nth-child(2) td').text
        browser.find_element_by_css_selector('a.btn.btn_red').click()
      except:
        price, account = (0, '')
      return insu, price, account
    types = ['health', 'pension', 'goyong', 'sanjae']
    result = [proc(self.browser, t) for t in types]
    return result
