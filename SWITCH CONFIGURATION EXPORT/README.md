# CISCO
---------------------------------------------------------------------------
NETWORK RELATED SCRIPTS

Authentication, Authorization, and Accounting (AAA)은 TACAS+, Radius 와같은 프로토콜을 사용하여 인증하는 방식이다.

대부분 시스코 스위치에 로그인하는 경우는 아래처럼 로그인한 후 enable 명령어를 사용하여 모든 명령어를 사용하여 인증하면 모든 명령어에 접근가능하다.

User Access Verification

Username: admin
Password:

Switch>en
Password:
Switch#
AAA를 사용하는경우 특정 권한을 부여하여 아래처럼 enable 상태로 바로 로그인 하도록 설정이 가능하다.

User Access Verification

Username: admin
Password:

Switch#
aaa를 사용가능하도록 설정하고 이름은 MGMT, 인증은 자체인증(local, 스위치에 설정된 username으로 인증)하도록 설정한다.

Switch#conf t

Switch(config)#aaa new-model
Switch(config)#aaa authentication login MGMT local
enable 비밀번호와 user/password를 설정한다(여기서는 enable 비밀번호와 admin 계정의 비밀번호 모두 admin123으로 설정)

Switch(config)#enable secret 0 admin123
Switch(config)#username admin privilege 15 password 0 admin123
telnet 접속 가능하도록 설정 하고, 로그인에 aaa를 이용하도록 설정.

Switch(config)#line vty 0 15
Switch(config-line)#login au
Switch(config-line)#login authentication MGMT
Switch(config-line)#transport input telnet
Switch(config-line)#exit
Switch(config)#aaa authentication login default enable
이제 privilege level을 15로 설정하면 enable 없이 바로 enable상태가 된다.

Switch(config)#line vty 0 15
Switch(config-line)#privilege level 15
Switch(config-line)#end

--- 
ver 0.0.1 

1. python-3.6.5를 설치한다.

2. command 창에서 아래 명령어 실행
pip install netmiko

pip install telnetlib

3. switch.txt화일에 스위치 접속정보를 입력한다.
각각의 열은 탭 키 하나로 구분한다(여럿으로 구분하면 오류발생함)

4. 스크립트를 실행하면, ipaddress.txt 화일로 스위치 설정이 저장된다.



6. 지원 장비
Cisco IOS 사용장비.(ssh, telnet 지원)
extreme EXOS 사용 장비(telnet 지원)


스위치 접속 정보화일(switch.txt)은 아래와 같은 포맷이며, 각 열은 탭(\t) 하나로 구분한다.

# IP		PORT	USER	PASSWD		PROTOCOL	VENDOR
172.16.10.1	23 	admin	password1	telnet	cisco
172.16.10.2	22	root	password2	ssh	cisco
172.16.10.3	23	admin	password3	telnet	extreme

스크립트는 파이썬3.5, windows10에서 테스트했음.
파이썬 설치후, 아래 명령어로 netmiko를 설치한다.

pip install netmiko
pip install telnetlib
