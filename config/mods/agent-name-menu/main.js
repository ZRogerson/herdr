import { View, div } from "gpui-kit";
import { props, closeOverlay, openOverlay, theme } from "herdr";
export default class AgentNameMenu extends View {
  render() {
    const t = theme(), p = props() ?? {};
    return div().p(5).bg(t.popover).rounded(7).child(
      div().id("rename-agent").px(10).py(8).rounded(4).text_size(13).text_color(t.foreground)
        .cursor_pointer().hover(s => s.bg(t.hover)).child("Rename…")
        .on_click(() => {
          closeOverlay(p.overlay);
          openOverlay({ mod: "agent-name-prompt", kind: "dialog", width: 380, height: 240,
            props: { agentKey: p.agentKey, value: p.value, title: "Rename agent", hint: "Leave blank to use the agent’s reported title." } });
        }));
  }
}
