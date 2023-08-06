# -*- coding: utf-8 -*-

from win32com.client import Dispatch

class ComApi:
    
    """ Com接口说明

    from winmail import ComApi as WinmailCom

    wc = WinmailCom()
    winmail_db_path = wc.get_db_path()
    add_domain = wc.add_domain('test.com')
    print(add_domain)
    """
    
    def __init__(self) -> None:
        self.dll = Dispatch("MailServerCtrl.MailDBInterface")
        # init COM
        self.dll.InitControl("")
        self.winmail_path = self.dll.GetDBPath()

    def get_db_path(self) -> str:
        # Get Winmail path
        winmail_path = self.dll.GetDBPath()
        return winmail_path

    def add_domain(self, strDomain) -> int:

        return self.dll.AddDomain(strDomain)

    def modify_domain(self,
                     strDomain,
                     strNTDomain,
                     strHost, 
                     strIP, 
                     strAdmin,
                     uRegister, 
                     uConfirm) -> int:

        return self.dll.ModifyDomain(strDomain, strNTDomain, strHost, strIP, strAdmin, uRegister, uConfirm)

    def modify_domain_right(self, 
                          strDomain, 
                          lExpireTime, 
                          uPop3Control,
                          uImapControl,
                          uWebmailControl, 
                          uNetStoreControl,
                          uCalendarControl, 
                          uNotebookControl,
                          uExternalPop3
                          ) -> int:

        return self.dll.ModifyDomainRight(strDomain, lExpireTime, uPop3Control, uImapControl, uWebmailControl, uNetStoreControl, uCalendarControl, uNotebookControl, uExternalPop3)

    def delete_domain(self, strDomain) -> int:

        return self.dll.DeleteDomain(strDomain)

    def add_user(self, strDomain, strUser, strPassword) -> int:

        return self.dll.AddUser(strUser, strDomain, strPassword)

    def modify_user_quota(self, 
                        strUser, 
                        strDomain, 
                        lMailQuota, 
                        iMailTotalLimit, 
                        iWarningLimit, 
                        lNetStoreQuota,
                        iNetStoreTotalLimit
                        ) -> int:

        return self.dll.ModifyUserQuota(strUser, strDomain, lMailQuota, iMailTotalLimit, iWarningLimit, lNetStoreQuota, iNetStoreTotalLimit)

    def delete_user(self, strUser, strDomain) -> int:

        return self.dll.DeleteUser(strUser, strDomain)

    def check_user(self, strUser,  strDomain):

        return self.dll.CheckUser(strUser,  strDomain)

    def modify_domain(self,
                     strDomain,
                     strNTDomain,
                     strHost,
                     strIP,
                     strAdmin,
                     uRegister,
                     uConfirm
                     ) -> int:

        return self.dll.ModifyDomain(strDomain, strNTDomain, strHost, strIP, strAdmin, uRegister, uConfirm)

    def modify_user(self,
                   strUser,
                   strDomain,
                   strFullName,
                   strDescription,
                   strCompany,
                   strOffice
                   ) -> int:

        return self.dll.ModifyUser(strUser, strDomain, strFullName, strDescription, strCompany, strOffice)

    def modify_user1(self, 
                    pstrUser, 
                    pstrDomain, 
                    pstrMobile, 
                    pstrHomePhone,
                    pstrHomeAddress, 
                    pstrJobTitle, 
                    pstrOfficePhone) -> int:

        return self.dll.ModifyUser1(pstrUser, pstrDomain, pstrMobile, pstrHomePhone, pstrHomeAddress, pstrJobTitle, pstrOfficePhone)

