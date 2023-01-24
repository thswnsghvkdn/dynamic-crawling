$(document).ready(function(){
    $('#Progress_Loading').hide(); //첫 시작시 로딩바를 숨겨준다.
 })
 .ajaxStart(function(){
     $('#Progress_Loading').show(); //ajax실행시 로딩바를 보여준다.
 })
 .ajaxStop(function(){
     $('#Progress_Loading').hide(); //ajax종료시 로딩바를 숨겨준다.
 });


$(document).ready(function(){
    // DB 에 TEST CASE 에 대한 XPATH 들을 이미 저장되어있기에 선택시 XPATH 들을 불러온다.
    $("#test-case").change(function() {
        // 테스트 케이스가 아닌 직접 사이트 XPATH를 입력할 경우 INPUT 태그들 초기화
        if($("#test-case").val() == "direct") {
			initInputValue()
		} else { 
            // 테스트 케이스의 XPATH를 불러온다.
            $.ajax({
                url: 'site-list/',
                type: 'GET',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    siteName: $("#test-case").val()
                },
                success: function(response){
                    $('input[id=site-name]').val(response.siteXpath[0]['site_name'])
                    $('input[id=site-url]').val(response.siteXpath[0]['url'])
                    $('input[id=link-list]').val(response.siteXpath[0]['link_list'])
                    $('input[id=published-date]').val(response.siteXpath[0]['published_date'])
                    $('input[id=title]').val(response.siteXpath[0]['title'])
                    $('input[id=body]').val(response.siteXpath[0]['body'])
                    $('input[id=attachment-list]').val(response.siteXpath[0]['attachment_list'])
                    $('input[id=timezone]').val(response.siteXpath[0]['time_zone'])
                    $('#exclude').empty()
                    // 제외시킬 원소의 경우 여러개 일 수 있다
                    for(let i =0 ; i < response.excludeList.length ; i++) 
                    {
                        if(response.excludeList[i]) {
                            $('#exclude').append('<input type="text" name="exclude-element" value="'+response.excludeList[i]['exclude_element_xpath'] +'"class="form-control" style="width:30%;" />');
                        }
                    }
                }
            }); 
        }
	})
    // TIMEZONE 의 경우 DATEPARSE에 들어갈 유효한 옵션 값을 선택하도록 한다.
    $("#timezone-select").change(function() {
        updateTimezoneValue();
	})  
    // 크롤링 버튼 클릭시 크롤링 작업 서버에 요청
    $('#create').on('click', function(){
        // TODO : RESTAPI 업데이트 site name 직접입력일 경우 xpath 정보를 추가하고 그렇지 않다면 update
        let requstMethod = $('#timezone-select')[0].selectedIndex === 0 ? 'POST' : 'PUT';
        $.ajax({
            url: 'article/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                siteName: $('input[id=site-name]').val(),
                siteUrl: $('input[id=site-url]').val(),
                linkList: $('input[id=link-list]').val(),
                publishedDate: $('input[id=published-date]').val(),
                title: $('input[id=title]').val(),
                body: $('input[id=body]').val(),
                attachmentList: $('input[id=attachment-list]').val(),
                timezone : $('input[id=timezone]').val(),
                excludePathList: JSON.stringify(getExcludeList()),
                crawlingCount : getCrawlingCount()
            },
            success: function(){
                // TODO : 실패 테이블에 저장된 크롤링 실패 데이터 알림
                alert("크롤링 완료");
            }
        });
    });
    // 크롤링 이후 DB에 저장되어있는 정보 중 옵션에 선택되어 있는 SITE 이름의 것들 RENDER
    $('#read').on('click', function(){
        $.ajax({
            url: 'article/',
            type: 'GET',
            async: false,
            data:{
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                siteName: $('input[id=site-name]').val()
            },
            success: function(response){
                $('#result').empty()
                for(let i = 0 ; i < response.length ; i++) {
                    if(response[i]) {
                        $('#result').append('<h5>title</h5>');
                        $('#result').append(response[i].fields.title);
                        $('#result').append('<h5>published_date</h5>');
                        $('#result').append(response[i].fields.published_datetime);
                        $('#result').append('<h5>body</h5>');
                        $('#result').append(response[i].fields.body);
                        $('#result').append('<h5>attachment</h5>');
                        $('#result').append(response[i].fields.attachment_list);
                        $('#result').append('<hr width = "100%" color = "black" size = "3">');
                    }
                }
            }
        });
    });
    // 제외 시킬 원소가 1개 이상일 경우 INPUT 태그 추가
    $('#add-exclude').on('click', function(){
        $('#exclude').append('<input type="text" name="exclude-element" class="form-control" style="width:30%;" />');
    });
    // 본초 자오선 기준 시간차이에 대한 그림을 TOOLTIP으로 보여준다.
    $('input[data-toggle="tooltip"]').tooltip({
        animated: 'fade',
        placement: 'right',
        html: true
    });
    $('select[data-toggle="tooltip"]').tooltip({
        animated: 'fade',
        placement: 'right',
        html: true
    });
    // TIMEZONE 옵션 RENDER
    renderTimezoneOption();
    updateTimezoneValue();
});
/** body html 중  사용자가 input tag 에 입력한 제외될 원소리스트 전부를 반환합니다. */
function getExcludeList() {
    let excludeList = [];
    let excludeInputTags = document.getElementsByName('exclude-element');
    for(let i = 0 ; i < excludeInputTags.length ; i++) {
        excludeList.push(excludeInputTags[i].value);
    }
    return excludeList;
}
/** 본초 자오선 기준 시간의 차이들을 입력받기 위해 -12:00 ~ +12:00로 옵션을 구성합니다.  */
function renderTimezoneOption() {
    let timezones = []
    let digit = ''
    let selected = ''
    for(let num = 12 ; num >= 0 ; num--)
    {
        digit = '0' + num.toString() + ':00'
        timezones.push('-' + digit.slice(-5) )
    }
    for(let num = 1 ; num <= 12 ; num++ )
    {
        digit = '0' + num.toString() + ':00'
        timezones.push('+' + digit.slice(-5) )
    }
    for(let i =0 ; i < timezones.length; i++) {
        if(timezones[i] === '+09:00'){
            selected = 'selected'
        } else {
            selected = ''
        }
        $('option[value=timezone]').after('<option class="timezone" '+ selected +'>'+ timezones[i] + '</option>');
    }
}
/** timezone 옵션 선택된 값으로  input value로 업데이트 합니다 */
function updateTimezoneValue(){
    let timezoneTag = $('#timezone-select')[0];
    let selectedIndexOrKST = timezoneTag.selectedIndex === 0 ? 4 : timezoneTag.selectedIndex; // TIMEZONE 을 선택할경우 KST 가 위치한 인덱스인 4번을 가리킨다.
    $('input[id=timezone]').val(timezoneTag.options[selectedIndexOrKST].value);
}
/** 모든 input 태그 들의 값을 비웁니다. */
function initInputValue() {
    let allInputTag = $('input')
    for(let i = 1 ; i < allInputTag.length ; i++) {
        allInputTag[i].value = null
    }
    $('#exclude').empty()
 }
 /** 선택한 크롤링 카운트 반환 */
function getCrawlingCount(){
    let crawlingCountSelect = $('#clawling-count')[0];
    return crawlingCountSelect.options[crawlingCountSelect.selectedIndex].value;
}