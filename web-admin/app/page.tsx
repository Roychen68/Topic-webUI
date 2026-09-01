'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';

type ViewName = '總覽' | '目標與排程' | 'Discord 紀錄' | '成效分析' | '成員管理';
type Goal = {
  id: number;
  title: string;
  target: string;
  progress: number;
  streak: number;
  status: '進行中' | '今日完成' | '尚未開始';
};
type RecordTab = '最近紀錄' | '介入活動' | '連續達標';

const navItems: Array<{ icon: string; label: ViewName }> = [
  { icon: 'bi-grid-1x2', label: '總覽' },
  { icon: 'bi-bullseye', label: '目標與排程' },
  { icon: 'bi-discord', label: 'Discord 紀錄' },
  { icon: 'bi-bar-chart', label: '成效分析' },
  { icon: 'bi-people', label: '成員管理' },
];

const initialGoals: Goal[] = [
  { id: 1, title: '每天完成 3 小時深度專注', target: '每日 · 180 分鐘', progress: 72, streak: 12, status: '進行中' },
  { id: 2, title: '本週完成投資簡報', target: '本週 · 6 個任務', progress: 67, streak: 4, status: '進行中' },
  { id: 3, title: '晚上 11 點前離開遊戲', target: '每日 · 22:50 提醒', progress: 100, streak: 8, status: '今日完成' },
];

const schedule = [
  { time: '08:30', title: '整理 Discord Bot 待辦流程', duration: '50 分鐘', state: '完成' },
  { time: '10:00', title: '完成投資簡報產品策略頁', duration: '90 分鐘', state: '專注中' },
  { time: '13:30', title: '硬體原型規格討論', duration: '60 分鐘', state: '待開始' },
  { time: '16:00', title: '整理使用者訪談筆記', duration: '40 分鐘', state: '待開始' },
];

const activityRecords: Record<RecordTab, Array<{ icon: string; tone: string; title: string; meta: string; streak?: string; badge?: string }>> = {
  最近紀錄: [
    { icon: 'bi-controller', tone: 'orange', title: 'League of Legends', meta: '5 小時前', badge: '專注時段內' },
    { icon: 'bi-file-earmark-slides', tone: 'indigo', title: '完成投資簡報產品策略頁', meta: '昨天 · 專注 48 分鐘', streak: '12 天連續達標' },
    { icon: 'bi-youtube', tone: 'red', title: 'YouTube', meta: '昨天 · 停留 3 分 12 秒', badge: '已記錄' },
    { icon: 'bi-check2-circle', tone: 'green', title: 'Discord Bot 待辦流程', meta: '2 天前 · 已完成', streak: '本週第 4 個任務' },
  ],
  介入活動: [
    { icon: 'bi-shield-exclamation', tone: 'red', title: '偵測到 League of Legends', meta: '10:18 · 已發送 Discord 警告', badge: '12 秒後離開' },
    { icon: 'bi-hourglass-split', tone: 'orange', title: 'YouTube 超過允許時間', meta: '昨天 09:42 · 已啟動分心計時', badge: '已列入週報' },
    { icon: 'bi-plus-circle', tone: 'indigo', title: '任務延長 10 分鐘', meta: '昨天 16:40 · User 主動延長', badge: '已同步' },
  ],
  連續達標: [
    { icon: 'bi-lightning-charge-fill', tone: 'yellow', title: '每日深度專注', meta: '今天更新', streak: '12 天 Streak' },
    { icon: 'bi-moon-stars', tone: 'indigo', title: '晚上 11 點前離開遊戲', meta: '昨天更新', streak: '8 天 Streak' },
    { icon: 'bi-check-all', tone: 'green', title: '每週完成 6 個任務', meta: '本週進度 4 / 6', streak: '連續 4 週' },
  ],
};

const members = [
  { name: 'User', handle: '@user', score: 82, focus: '18h 42m', state: '專注中', initials: 'U' },
  { name: 'Member 02', handle: '@member02', score: 76, focus: '15h 08m', state: '在線', initials: '02' },
  { name: 'Member 03', handle: '@member03', score: 91, focus: '22h 16m', state: '專注中', initials: '03' },
  { name: 'Member 04', handle: '@member04', score: 68, focus: '11h 43m', state: '離線', initials: '04' },
];

function formatTimer(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const rest = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${rest}`;
}

export default function Home() {
  const [activeView, setActiveView] = useState<ViewName>('總覽');
  const [goals, setGoals] = useState<Goal[]>(initialGoals);
  const [secondsLeft, setSecondsLeft] = useState(42 * 60 + 18);
  const [modalOpen, setModalOpen] = useState(false);
  const [toast, setToast] = useState('');
  const [recordTab, setRecordTab] = useState<RecordTab>('最近紀錄');
  const [rules, setRules] = useState({ games: true, entertainment: true, autoExtend: false });

  useEffect(() => {
    const timer = window.setInterval(() => setSecondsLeft((value) => Math.max(0, value - 1)), 1000);
    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    if (!toast) return;
    const timeout = window.setTimeout(() => setToast(''), 2600);
    return () => window.clearTimeout(timeout);
  }, [toast]);

  useEffect(() => {
    if (!modalOpen) return;
    const close = (event: KeyboardEvent) => event.key === 'Escape' && setModalOpen(false);
    window.addEventListener('keydown', close);
    return () => window.removeEventListener('keydown', close);
  }, [modalOpen]);

  const heading = useMemo(() => activeView === '總覽' ? '早安，User' : activeView, [activeView]);

  function navigate(view: ViewName) {
    setActiveView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function createGoal(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const title = String(data.get('title') || '新的專注目標');
    const period = String(data.get('period') || '每日');
    const minutes = String(data.get('minutes') || '60');
    setGoals((current) => [
      ...current,
      { id: Date.now(), title, target: `${period} · ${minutes} 分鐘`, progress: 0, streak: 0, status: '尚未開始' },
    ]);
    setModalOpen(false);
    setToast(`目標「${title}」已建立`);
  }

  function toggleRule(key: keyof typeof rules) {
    setRules((current) => ({ ...current, [key]: !current[key] }));
    setToast('Discord 介入規則已更新');
  }

  return (
    <div className="app-layout">
      <aside className="app-sidebar">
        <button className="sidebar-brand" onClick={() => navigate('總覽')} aria-label="回到總覽">
          <span className="brand-logo"><i className="bi bi-discord" /></span>
          <span><strong>Concentrate</strong><small>Discord Focus Bot</small></span>
        </button>

        <nav className="nav nav-pills flex-column gap-1" aria-label="主要導覽">
          <span className="sidebar-label">管理選單</span>
          {navItems.map((item) => (
            <button
              key={item.label}
              className={`nav-link d-flex align-items-center gap-3 ${activeView === item.label ? 'active' : ''}`}
              onClick={() => navigate(item.label)}
            >
              <i className={`bi ${item.icon}`} />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="connection-panel mt-auto">
          <div className="d-flex align-items-center gap-2"><span className="status-dot" /><strong>Bot 已連線</strong></div>
          <small>每 10 秒同步一次狀態</small>
        </div>
        <div className="user-panel">
          <span className="user-avatar">U</span>
          <span><strong>User</strong><small>管理員</small></span>
          <i className="bi bi-three-dots ms-auto" />
        </div>
      </aside>

      <main className="main-panel">
        <header className="app-header navbar bg-white border-bottom">
          <div>
            <small className="text-uppercase text-secondary fw-semibold">Control Room / {activeView}</small>
            <h1>{heading}</h1>
          </div>
          <div className="d-flex align-items-center gap-2">
            <span className="sync-badge d-none d-md-inline-flex"><span className="status-dot" />Discord 同步中</span>
            <button className="btn btn-light border icon-btn" aria-label="通知" onClick={() => setToast('目前沒有未讀通知')}><i className="bi bi-bell" /></button>
            <button className="btn btn-primary" onClick={() => setModalOpen(true)}><i className="bi bi-plus-lg me-1" />建立目標</button>
          </div>
        </header>

        <section className="container-fluid content-area">
          {activeView === '總覽' && (
            <Overview
              secondsLeft={secondsLeft}
              goals={goals}
              recordTab={recordTab}
              setRecordTab={setRecordTab}
              onNavigate={navigate}
              onCreateGoal={() => setModalOpen(true)}
              setToast={setToast}
            />
          )}
          {activeView === '目標與排程' && <Goals goals={goals} onCreate={() => setModalOpen(true)} />}
          {activeView === 'Discord 紀錄' && <DiscordRecords recordTab={recordTab} setRecordTab={setRecordTab} rules={rules} toggleRule={toggleRule} />}
          {activeView === '成效分析' && <Analytics />}
          {activeView === '成員管理' && <Members setToast={setToast} />}
        </section>
      </main>

      {modalOpen && (
        <div className="modal d-block goal-modal" tabIndex={-1} role="dialog" aria-modal="true" onMouseDown={(event) => event.target === event.currentTarget && setModalOpen(false)}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <form onSubmit={createGoal}>
                <div className="modal-header">
                  <div><small className="text-uppercase text-secondary fw-semibold">New goal</small><h2 className="modal-title fs-5">建立目標</h2></div>
                  <button type="button" className="btn-close" aria-label="關閉" onClick={() => setModalOpen(false)} />
                </div>
                <div className="modal-body">
                  <div className="mb-3"><label className="form-label">目標名稱</label><input className="form-control" name="title" placeholder="例如：每天專心讀書 2 小時" autoFocus required /></div>
                  <div className="row g-3 mb-3">
                    <div className="col-sm-6"><label className="form-label">週期</label><select className="form-select" name="period" defaultValue="每日"><option>每日</option><option>每週</option><option>自訂期間</option></select></div>
                    <div className="col-sm-6"><label className="form-label">目標時間</label><select className="form-select" name="minutes" defaultValue="60"><option value="30">30 分鐘</option><option value="60">60 分鐘</option><option value="120">120 分鐘</option><option value="180">180 分鐘</option></select></div>
                  </div>
                  <div className="form-check form-switch mb-3"><input className="form-check-input" type="checkbox" id="intervention" defaultChecked /><label className="form-check-label" htmlFor="intervention">啟用 Discord 分心偵測與介入</label></div>
                  <div className="alert alert-primary d-flex gap-2 mb-0" role="note"><i className="bi bi-discord" /><small>建立後，Bot 會透過 Discord 回報每日進度與連續達標紀錄。</small></div>
                </div>
                <div className="modal-footer"><button type="button" className="btn btn-light border" onClick={() => setModalOpen(false)}>取消</button><button className="btn btn-primary" type="submit">建立目標</button></div>
              </form>
            </div>
          </div>
        </div>
      )}

      {toast && <div className="toast show align-items-center text-bg-dark border-0 app-toast" role="status"><div className="d-flex"><div className="toast-body"><i className="bi bi-check-circle-fill text-success me-2" />{toast}</div></div></div>}
    </div>
  );
}

function Overview({ secondsLeft, goals, recordTab, setRecordTab, onNavigate, onCreateGoal, setToast }: {
  secondsLeft: number;
  goals: Goal[];
  recordTab: RecordTab;
  setRecordTab: (tab: RecordTab) => void;
  onNavigate: (view: ViewName) => void;
  onCreateGoal: () => void;
  setToast: (value: string) => void;
}) {
  return (
    <div className="row g-3">
      <div className="col-xl-8">
        <section className="card focus-session-card h-100">
          <div className="card-body p-4">
            <div className="d-flex align-items-center justify-content-between mb-4"><span className="badge rounded-pill text-bg-success"><span className="live-dot" />專注進行中</span><button className="btn btn-sm btn-outline-light" onClick={() => onNavigate('Discord 紀錄')}>介入設定</button></div>
            <div className="row align-items-center g-4">
              <div className="col-md"><small className="text-uppercase opacity-50 fw-semibold">目前目標</small><h2>本週完成投資簡報</h2><p className="mb-0 opacity-75"><i className="bi bi-clock me-2" />10:00–11:30　<i className="bi bi-discord me-2" />#deep-work</p></div>
              <div className="col-md-auto"><div className="countdown"><strong>{formatTimer(secondsLeft)}</strong><small>剩餘時間</small></div></div>
            </div>
          </div>
          <div className="card-footer focus-footer"><i className="bi bi-shield-check me-2" /><strong>強制介入已啟用</strong><span className="ms-2">偵測到非白名單遊戲時會立即通知</span></div>
        </section>
      </div>

      <div className="col-xl-4">
        <section className="card h-100 summary-card">
          <div className="card-body p-4"><div className="d-flex justify-content-between"><div><small className="text-secondary text-uppercase fw-semibold">今日表現</small><h2 className="h5 mt-1">專注摘要</h2></div><span className="badge text-bg-light align-self-start text-success">↑ 12%</span></div><div className="summary-score">82 <small>/100</small></div><div className="progress" role="progressbar" aria-label="今日專注分數" aria-valuenow={82} aria-valuemin={0} aria-valuemax={100}><div className="progress-bar" style={{ width: '82%' }} /></div><p className="text-secondary small mt-3 mb-4">比過去 7 天的平均高 9 分。</p><div className="row g-2"><div className="col"><div className="stat-box"><small>完成目標</small><strong>2 / 3</strong></div></div><div className="col"><div className="stat-box"><small>專注時間</small><strong>3h 24m</strong></div></div></div></div>
        </section>
      </div>

      <div className="col-xl-7">
        <DiscordFrame recordTab={recordTab} setRecordTab={setRecordTab} compact />
      </div>

      <div className="col-xl-5">
        <section className="card h-100">
          <div className="card-header bg-white d-flex align-items-center justify-content-between"><div><small className="text-secondary text-uppercase fw-semibold">Goals</small><h2 className="h5 mb-0">我的目標</h2></div><button className="btn btn-sm btn-outline-primary" onClick={onCreateGoal}><i className="bi bi-plus-lg me-1" />新增</button></div>
          <div className="list-group list-group-flush goal-summary-list">
            {goals.slice(0, 3).map((goal) => <div className="list-group-item" key={goal.id}><div className="d-flex align-items-start justify-content-between gap-2"><div><strong>{goal.title}</strong><small>{goal.target}</small></div><span>{goal.progress}%</span></div><div className="progress mt-2"><div className="progress-bar" style={{ width: `${goal.progress}%` }} /></div></div>)}
          </div>
          <div className="card-footer bg-white"><button className="btn btn-link btn-sm p-0 text-decoration-none" onClick={() => onNavigate('目標與排程')}>管理所有目標 <i className="bi bi-arrow-right" /></button></div>
        </section>
      </div>

      <div className="col-lg-8">
        <section className="card h-100">
          <div className="card-header bg-white d-flex justify-content-between align-items-center"><div><small className="text-secondary text-uppercase fw-semibold">Weekly focus</small><h2 className="h5 mb-0">本週專注時數</h2></div><span className="fw-semibold">18h 42m</span></div>
          <div className="card-body"><div className="bootstrap-chart" aria-label="本週專注時數長條圖">{[42,58,48,76,65,88,72].map((height, index) => <div className="chart-column" key={index}><span style={{ height: `${height}%` }} className={index === 5 ? 'active' : ''} /><small>{['一','二','三','四','五','六','日'][index]}</small></div>)}</div></div>
        </section>
      </div>
      <div className="col-lg-4">
        <section className="card h-100"><div className="card-body p-4"><div className="d-flex align-items-center gap-2 mb-3"><span className="ai-icon"><i className="bi bi-stars" /></span><div><small className="text-secondary text-uppercase fw-semibold">Routine 建議</small><h2 className="h6 mb-0">調整明日排程</h2></div></div><p className="small text-secondary">User 的高效率區間集中在 09:30–11:00，建議把產品規劃提前 30 分鐘。</p><button className="btn btn-sm btn-primary" onClick={() => setToast('明日排程已更新')}>套用建議</button></div></section>
      </div>
    </div>
  );
}

function DiscordFrame({ recordTab, setRecordTab, compact = false }: { recordTab: RecordTab; setRecordTab: (tab: RecordTab) => void; compact?: boolean }) {
  const records = compact ? activityRecords[recordTab].slice(0, 3) : activityRecords[recordTab];
  return (
    <section className="card discord-frame h-100">
      <div className="discord-frame-header">
        <div className="d-flex align-items-center gap-2"><span className="discord-logo"><i className="bi bi-discord" /></span><div><strong>Discord 活動紀錄</strong><small>Concentrate Bot · 已連線</small></div></div>
        <span className="badge text-bg-success">LIVE</span>
      </div>
      <div className="discord-tabs" role="tablist">
        {(Object.keys(activityRecords) as RecordTab[]).map((tab) => <button key={tab} className={recordTab === tab ? 'active' : ''} onClick={() => setRecordTab(tab)} role="tab" aria-selected={recordTab === tab}>{tab}</button>)}
      </div>
      <div className="discord-record-list">
        {records.map((record) => (
          <article className="discord-record" key={`${recordTab}-${record.title}`}>
            <span className={`record-icon tone-${record.tone}`}><i className={`bi ${record.icon}`} /></span>
            <div><strong>{record.title}</strong><p><i className="bi bi-controller" /> {record.meta}{record.streak && <><i className="bi bi-lightning-charge-fill ms-3" /> {record.streak}</>}</p></div>
            {record.badge && <span className="record-badge">{record.badge}</span>}
            <button className="record-menu" aria-label={`${record.title} 更多選項`}><i className="bi bi-three-dots" /></button>
          </article>
        ))}
      </div>
    </section>
  );
}

function Goals({ goals, onCreate }: { goals: Goal[]; onCreate: () => void }) {
  return (
    <div className="row g-3">
      <div className="col-12"><div className="d-flex align-items-center justify-content-between mb-1"><div><h2 className="h4 mb-1">我的目標</h2><p className="text-secondary small mb-0">設定可量化的目標，Bot 會每天追蹤並回報。</p></div><button className="btn btn-primary" onClick={onCreate}><i className="bi bi-plus-lg me-1" />建立目標</button></div></div>
      {goals.map((goal) => (
        <div className="col-md-6 col-xl-4" key={goal.id}>
          <article className="card goal-card h-100"><div className="card-body"><div className="d-flex justify-content-between align-items-start"><span className="goal-icon"><i className="bi bi-bullseye" /></span><button className="btn btn-sm btn-light" aria-label={`${goal.title} 更多選項`}><i className="bi bi-three-dots" /></button></div><h3 className="h6 mt-3">{goal.title}</h3><p className="small text-secondary">{goal.target}</p><div className="d-flex justify-content-between small mb-2"><span>目前進度</span><strong>{goal.progress}%</strong></div><div className="progress"><div className="progress-bar" style={{ width: `${goal.progress}%` }} /></div><div className="d-flex justify-content-between align-items-center mt-3"><span className={`badge ${goal.status === '今日完成' ? 'text-bg-success' : 'text-bg-light'}`}>{goal.status}</span><span className="small text-secondary"><i className="bi bi-lightning-charge-fill text-warning" /> {goal.streak} 天</span></div></div></article>
        </div>
      ))}
      <div className="col-12 mt-4"><section className="card"><div className="card-header bg-white"><small className="text-secondary text-uppercase fw-semibold">Today</small><h2 className="h5 mb-0">今日排程</h2></div><div className="table-responsive"><table className="table align-middle mb-0 schedule-table"><thead><tr><th>開始時間</th><th>專注項目</th><th>持續時間</th><th>Discord 監督</th><th>狀態</th></tr></thead><tbody>{schedule.map((item) => <tr key={item.time}><td className="fw-semibold">{item.time}</td><td>{item.title}</td><td>{item.duration}</td><td><i className="bi bi-discord text-primary me-1" />已啟用</td><td><span className={`badge ${item.state === '完成' ? 'text-bg-success' : item.state === '專注中' ? 'text-bg-primary' : 'text-bg-light'}`}>{item.state}</span></td></tr>)}</tbody></table></div></section></div>
    </div>
  );
}

function DiscordRecords({ recordTab, setRecordTab, rules, toggleRule }: { recordTab: RecordTab; setRecordTab: (tab: RecordTab) => void; rules: { games: boolean; entertainment: boolean; autoExtend: boolean }; toggleRule: (key: keyof typeof rules) => void }) {
  return (
    <div className="row g-3">
      <div className="col-xl-8"><DiscordFrame recordTab={recordTab} setRecordTab={setRecordTab} /></div>
      <div className="col-xl-4"><section className="card h-100"><div className="card-header bg-white"><small className="text-secondary text-uppercase fw-semibold">Automation</small><h2 className="h5 mb-0">介入規則</h2></div><div className="list-group list-group-flush rule-list"><RuleRow icon="bi-controller" title="遊戲啟動" description="非白名單遊戲立即警告" active={rules.games} onClick={() => toggleRule('games')} /><RuleRow icon="bi-youtube" title="娛樂影音" description="超過 3 分鐘時計入分心" active={rules.entertainment} onClick={() => toggleRule('entertainment')} /><RuleRow icon="bi-clock-history" title="自動延長" description="逾時時自動增加 10 分鐘" active={rules.autoExtend} onClick={() => toggleRule('autoExtend')} /></div><div className="card-body"><div className="alert alert-secondary small mb-0"><i className="bi bi-info-circle me-2" />Demo 目前以模擬資料顯示；接上 Bot API 後會同步真實活動。</div></div></section></div>
    </div>
  );
}

function RuleRow({ icon, title, description, active, onClick }: { icon: string; title: string; description: string; active: boolean; onClick: () => void }) {
  return <div className="list-group-item d-flex align-items-center gap-3"><span className="rule-icon"><i className={`bi ${icon}`} /></span><span className="flex-grow-1"><strong>{title}</strong><small>{description}</small></span><div className="form-check form-switch"><input className="form-check-input" type="checkbox" checked={active} onChange={onClick} aria-label={title} /></div></div>;
}

function Analytics() {
  return (
    <div className="row g-3">
      {[['總專注時數','18h 42m','↑ 14%'],['目標完成率','84%','↑ 6%'],['介入次數','7','↓ 3 次'],['連續達標','12 天','最佳 18 天']].map((item) => <div className="col-sm-6 col-xl-3" key={item[0]}><div className="card metric-card h-100"><div className="card-body"><small className="text-secondary">{item[0]}</small><strong>{item[1]}</strong><span>{item[2]} 本週</span></div></div></div>)}
      <div className="col-xl-8"><section className="card h-100"><div className="card-header bg-white"><small className="text-secondary text-uppercase fw-semibold">Focus quality</small><h2 className="h5 mb-0">效率分數趨勢</h2></div><div className="card-body"><div className="bootstrap-chart analytics-chart">{[62,74,55,86,78,93,71].map((height,index) => <div className="chart-column" key={index}><span style={{ height: `${height}%` }} className={index === 5 ? 'active' : ''}><em>{height}</em></span><small>{['一','二','三','四','五','六','日'][index]}</small></div>)}</div></div></section></div>
      <div className="col-xl-4"><section className="card h-100 routine-card"><div className="card-body p-4"><span className="ai-icon"><i className="bi bi-clock" /></span><small className="text-secondary text-uppercase fw-semibold d-block mt-4">Routine signal</small><h2 className="h5">User 的黃金時段</h2><strong className="golden-time">09:30–11:00</strong><p className="small text-secondary">這段時間平均完成率 92%，分心次數也最低。</p><hr /><p className="small mb-0">建議把最重要的目標排在上午，並預留 15 分鐘緩衝。</p></div></section></div>
    </div>
  );
}

function Members({ setToast }: { setToast: (value: string) => void }) {
  return (
    <div className="card"><div className="card-header bg-white d-flex align-items-center justify-content-between"><div><small className="text-secondary text-uppercase fw-semibold">Team space</small><h2 className="h5 mb-0">成員狀態</h2></div><button className="btn btn-sm btn-outline-primary" onClick={() => setToast('邀請連結已複製')}><i className="bi bi-person-plus me-1" />邀請成員</button></div><div className="table-responsive"><table className="table align-middle mb-0 member-table"><thead><tr><th>成員</th><th>本週專注</th><th>專注分數</th><th>狀態</th><th /></tr></thead><tbody>{members.map((member) => <tr key={member.handle}><td><div className="d-flex align-items-center gap-2"><span className="member-avatar">{member.initials}</span><span><strong>{member.name}</strong><small>{member.handle}</small></span></div></td><td>{member.focus}</td><td>{member.score}</td><td><span className={`badge ${member.state === '專注中' ? 'text-bg-primary' : member.state === '在線' ? 'text-bg-success' : 'text-bg-light'}`}>{member.state}</span></td><td><button className="btn btn-sm btn-light" aria-label={`${member.name} 更多選項`}><i className="bi bi-three-dots" /></button></td></tr>)}</tbody></table></div></div>
  );
}
