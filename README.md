# dynamic-crawling

동적 렌더링과 정적 렌더링 페이지 모두 소스 수정 없이 크롤링을 진행하기 위해 selenium을 이용하였습니다
selenium의 경우 bs4 보다 느리지만 해당 부분을 파이썬 multiprocessing 을 활용하여 해당 부분을 보완하였습니다. 
현재는 site의 링크들을 4개의 프로세스로 병렬 처리하도록 구성하였습니다


화면 구성은 다음과 같습니다.

![image](https://user-images.githubusercontent.com/60654232/214289155-e6d29b91-03f1-43b4-a407-bf30fda4bfae.png)


site name 태그는 해당 사이트의 이름을 구분하기 위해 입력받습니다.
site name select 의 옵션들은 이미 xpath 를 저장해둔 테스트 케이스들로 옵션을 선택하면 해당 사이트의 xpath 들이 전체 input에 자동으로 채워집니다 

![image](https://user-images.githubusercontent.com/60654232/214290015-bca24c44-0099-4064-9551-ce9d98b88b50.png)

각 input 태그들은 크롤링시 web driver 에 인수로 전달된 값들 입니다. 클래스이름이나 아이디는 난수로 설정되는 경우가 있기 때문에 
테스트 케이스에서는 full xpath 를 이용하였습니다.

![image](https://user-images.githubusercontent.com/60654232/214290811-60be0f76-94f9-44d6-934a-ac2e3994f7d7.png)

a tag list 의 이름을 갖는 input tag 는 맨 처음 site url 에 접근을 하여 크롤링할 a href 들을 가져오기 위해 각 링크를 갖는 태그의 xpath를 입력받습니다. 
이때에 a tag 위치가 조금씩 다른데 이는 * 로 표시하여 페이지에 존재하는 모든 a 태그들을 수집합니다. 

![image](https://user-images.githubusercontent.com/60654232/214291622-de981390-49d1-4b61-b4a6-38c32c302f1a.png)

수집된 a 태그들을 몇개씩 가져오는지는 옵션으로 선택받도록 하였습니다. 
이때에 5개씩 받을 경우 처음 5개 링크들을 크롤링 한 이후에 다시 한번 5개씩 크롤링 할 경우 링크 리스트중 DB에서 이미 크롤링한 링크들을 조회하여 크롤링 되지 않은 링크들 중 
5개의 링크들에 대해 다시 크롤링을 진행합니다.

![image](https://user-images.githubusercontent.com/60654232/214292307-c83c3830-44f4-4f2a-8155-6918a301ea2b.png)

TIMEZONE에 경우 
PYTHON DATEPARSER에 본초 자오선을 기준 차이를 이용하는 옵션을 활용하기 위해 해당 DATEPARSER에 유효한 옵션값을 SELECT 로 입력받도록 하였고 
옵션에 마우스를 올릴 경우 툴팁으로 각 나라의 본초 자오선과의 시차를 확인할 수 있도록 하였습니다.

![image](https://user-images.githubusercontent.com/60654232/214293008-0b4e541c-5849-419a-a2d4-fc98f6132397.png)

제외할 원소의 XPATH를 입력 받아 해당 원소는 크롤링 이전에 JS 명령어로 삭제한 이후 크롤링 하여 필요없는 원소는 크롤링 되지 않도록 하였습니다.

![image](https://user-images.githubusercontent.com/60654232/214293538-a75b638e-24bf-455e-a6eb-7b20adf01ed1.png)


read 버튼 클릭시 DB 에 저장된 크롤링 된 데이터중 SITE NAME 태그에 입력되어 있는 SITE NAME 의 데이터들만 가져와 보여줍니다.

![image](https://user-images.githubusercontent.com/60654232/214294217-84ac3d59-9bb7-4110-9f28-9103eacf2317.png)


