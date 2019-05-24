package cn.leancloud.play.plugin.template;

import cn.leancloud.play.plugin.BoundRoom;
import cn.leancloud.play.plugin.GamePlugin;
import cn.leancloud.play.plugin.PluginFactory;
import cn.leancloud.play.utils.Log;

import java.util.Map;

public class MyFancyPluginFactory implements PluginFactory {
    @Override
    public GamePlugin create(BoundRoom room, String pluginName, Map<String, Object> initConfigs) {
        if (pluginName != null && pluginName.length() > 0) {
            switch (pluginName) {
                case "fancy-plugin":
                    return new MyFancyGamePlugin(room, initConfigs);
                case "master is watching you plugin":
                    return new MasterIsWatchingYouPlugin(room);
            }
        }

        Log.error("unknown plugin name {}", pluginName);
        return null;
    }
}
