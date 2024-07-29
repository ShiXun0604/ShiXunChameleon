## 簡介
* 此repository密碼學部分沒有使用外部crypt library，在Evaluate使用matplotlib進行畫圖資料分析。
* 此密碼學方法為我的碩士論文實作，source code有快比原始碼還長的註解可進行參考。
* 此package比較著重在觀察密碼學運作流程，未進行完整優化和正規化，不建議使用在production環境當中。

## 注意事項
* 開發版本：python 3.12.4
* 外部引用：random、hashlib、base64、matplotlib

## 安裝方法
可以直接在cmd透過pip進行安裝：
```
>>> pip install ShiXunChameleon
```

## SIS碰撞
此package包含基本的SIS碰撞函式，首先定義SIS基本參數n、q、sigma。其中n是向量維度、q是質數、l在實作SIS碰撞中不會用到隨意指定即可、sigma是取高斯矩陣時的標準差。經過實驗建議sigma取0.35。
```python
config.set_parameter(n=3, q=13, l=len(ID), sigma=0.3)
```

使用gen_A_with_trapdoor生成帶有trapdoor的矩陣A：
```python
A, R = BasicSIS.gen_A_with_trapdoor()
```

接著使用gen_x隨意舉任意短向量x，並且計算雜湊值u：
```python
x = BasicSIS.gen_x()
u = (A * x) % para.q
```

若有trapdoor R，可以使用inverse_SIS算出另一個x2使得雜湊碰撞u=u2成立：
```python
x2 = BasicSIS.inverse_SIS(A, u, R)
u2 = (A * x2) % para.q
```

## ShiXunChameleon

### １. setup phase

我的論文提出一種ID base的變色龍雜湊，首先定義基本參數，其中n是向量維度、q是質數、l是ID訊息的bit數、sigma是取高斯矩陣時的標準差，經過實驗建議sigma取0.35：
```python
ID='101'
config.set_parameter(n=3, q=13, l=len(ID), sigma=0.3)
```

系統中包含一個CA以及多個User。首先CA必須生成其公、私鑰對MPK、MSK，生成後的公司鑰對儲存於該物件中：
```python
CA_obj = SXchameleonCA()
CA_obj.generate_MPK_MSK()
```

物件中extract_master_key、extract_master_private_key方法分別回傳該物件中的公鑰以及私鑰.pem格式的字串，接著可以使用open方法將公、私鑰字串寫入.pem檔中進行儲存管理：
```python
MPK_pem = CA_obj.extract_master_key()
with open('MPK.pem', 'wb') as f:
    f.write(MPK_pem)

MSK_pem = CA_obj.extract_master_private_key()
with open('MSK.pem', 'wb') as f:
    f.write(MSK_pem)
```

### 2. CA genegrate user SK phase

CA透過私鑰MSK可計算個別使用者的私鑰。若物件內未儲存私鑰的話，必須透過import_key方法將儲存在.pem中的私鑰載入物件中，再使用extract_user_private_key方法帶入user的身分訊息後回傳該user對應的pem格式密鑰：
```python
# 讀取MPK
CA_obj = SXchameleonCA()
with open('MSK.pem', 'rb') as f:
    MSK_pem = f.read()
CA_obj.import_key(MSK_pem)

# 生成並保存R_ID
R_ID_pem= CA_obj.extract_user_private_key(ID)
with open('SK_{}.pem'.format(ID), 'wb') as f:
    f.write(R_ID_pem)
```

### 3. Hashing phase

使用SXchameleonUser類別定義個別的使用者，宣告時必須帶入使用者的ID身分訊息：
```python
usr_obj = SXchameleonUser(ID)
```

使用import_MPK方法將CA公鑰匯入，該方法會自動的計算該使用者的公鑰並儲存於物件中。
```python
with open('MPK.pem', 'rb') as f:
    MPK_pem = f.read()
usr_obj.import_MPK(MPK_pem)
```

相同於SIS碰撞中的過程，此class將雜湊過程包含入物件中，hashing方法即可回傳雜湊值u。
```python
x = BasicSIS.gen_x()
u = usr_obj.hashing(x)
```

### 4. Forge phase

若擁有CA給出的私鑰，可以匯入CA給的私鑰後，計算x2使得雜湊碰撞u=u2成立：
```python
# 讀取並載入R_ID
with open('SK_{}.pem'.format(ID), 'rb') as f:
    R_ID_pem = f.read()
usr_obj.import_key(R_ID_pem)

# 計算雜湊碰撞
x2 = usr_obj.forge(u)
u2 = usr_obj.hashing(x2)
```
