#include "stdio.h"
#define API extern "C" __attribute__((visibility("default")))
typedef int(*PCMDCALLBACK)(int nTermIndex, char* chContent, long long nContext);
PCMDCALLBACK m_pCmdCallBack = 0;
long long m_Context = 0;

API int SetCmdCallBack(PCMDCALLBACK pcmdCB, long long Context)
{
	if (pcmdCB)
	{
		m_pCmdCallBack = pcmdCB;
	}
	else
	{
		return -1;
	}
	m_Context = Context;
	return 0;
}

API int ExeCmdCallBack(int nTermIndex, char* chContent)
{
	if (m_pCmdCallBack)
	{
		return m_pCmdCallBack(nTermIndex, chContent, m_Context);
	}
	else
	{
		return -1;
	}
}
