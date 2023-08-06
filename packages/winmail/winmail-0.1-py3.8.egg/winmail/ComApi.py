# -*- coding: utf-8 -*-

from win32com.client import Dispatch

class ComApi:
    def __init__(self) -> None:
        self.dll = Dispatch("MailServerCtrl.MailDBInterface")
        # init COM
        self.dll.InitControl("")
        self.winmail_path = self.dll.GetDBPath()

    def GetDBPath(self) -> str:
        # Get Winmail path
        winmail_path = self.dll.GetDBPath()
        return winmail_path

    def AddDomain(self, strDomain) -> int:

        return self.dll.AddDomain(strDomain)

    def ModifyDomain(self,
                     strDomain,
                     strNTDomain,
                     strHost, 
                     strIP, 
                     strAdmin,
                     uRegister, 
                     uConfirm) -> int:

        return self.dll.ModifyDomain(strDomain, strNTDomain, strHost, strIP, strAdmin, uRegister, uConfirm)

    def ModifyDomainRight(self, 
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

    def DeleteDomain(self, strDomain) -> int:

        return self.dll.DeleteDomain(strDomain)

    def AddUser(self, strDomain, strUser, strPassword) -> int:

        return self.dll.AddUser(strUser, strDomain, strPassword)

    def ModifyUserQuota(self, 
                        strUser, 
                        strDomain, 
                        lMailQuota, 
                        iMailTotalLimit, 
                        iWarningLimit, 
                        lNetStoreQuota,
                        iNetStoreTotalLimit
                        ) -> int:

        return self.dll.ModifyUserQuota(strUser, strDomain, lMailQuota, iMailTotalLimit, iWarningLimit, lNetStoreQuota, iNetStoreTotalLimit)

    def DeleteUser(self, strUser, strDomain) -> int:

        return self.dll.DeleteUser(strUser, strDomain)

    def CheckUser(self, strUser,  strDomain):

        return self.dll.CheckUser(strUser,  strDomain)

    def ModifyDomain(self,
                     strDomain,
                     strNTDomain,
                     strHost,
                     strIP,
                     strAdmin,
                     uRegister,
                     uConfirm
                     ) -> int:

        return self.dll.ModifyDomain(strDomain, strNTDomain, strHost, strIP, strAdmin, uRegister, uConfirm)

    def ModifyUser(self,
                   strUser,
                   strDomain,
                   strFullName,
                   strDescription,
                   strCompany,
                   strOffice
                   ) -> int:

        return self.dll.ModifyUser(strUser, strDomain, strFullName, strDescription, strCompany, strOffice)

    def ModifyUser1(self, 
                    pstrUser, 
                    pstrDomain, 
                    pstrMobile, 
                    pstrHomePhone,
                    pstrHomeAddress, 
                    pstrJobTitle, 
                    pstrOfficePhone) -> int:

        return self.dll.ModifyUser1(pstrUser, pstrDomain, pstrMobile, pstrHomePhone, pstrHomeAddress, pstrJobTitle, pstrOfficePhone)

